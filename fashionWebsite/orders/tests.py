from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from fashionWebsite.clothes.models import Garment, Product, Color, Size, Category
from fashionWebsite.orders.models import Order, OrderItem
from fashionWebsite.orders.utils import get_or_create_cart, update_order_total
from fashionWebsite.accounts.models import Customer
from decimal import Decimal

AppUser = get_user_model()


def create_test_garment():
    category = Category.objects.create(name="Test Category", slug="test-category")
    color = Color.objects.create(name="Red", hex_code="#ff0000")
    size = Size.objects.create(name="M")
    garment = Garment.objects.create(
        name="Test Dress",
        slug="test-dress",
        price=Decimal("50.00"),
    )
    garment.category.add(category)
    product = Product.objects.create(
        garment=garment,
        color=color,
        size=size,
        stock=10,
    )
    return garment, product


def create_complete_customer(user):
    customer, _ = Customer.objects.get_or_create(user=user)
    customer.first_name = "Jane"
    customer.last_name = "Doe"
    customer.address = "123 Main St"
    customer.telephone_number = "0612345678"
    customer.save()
    return customer


class OrderItemTest(TestCase):
    def setUp(self):
        self.user = AppUser.objects.create_user(
            email="test@example.com",
            password="testpass123",
        )
        _, self.product = create_test_garment()
        self.order = Order.objects.create(
            customer=self.user,
            status="pending",
            total_amount=Decimal("0.00"),
        )

    def test_line_total(self):
        item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=3,
            unit_price=Decimal("50.00"),
        )
        self.assertEqual(item.line_total, Decimal("150.00"))

    def test_update_order_total(self):
        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            unit_price=Decimal("50.00"),
        )
        update_order_total(self.order)
        self.order.refresh_from_db()
        self.assertEqual(self.order.total_amount, Decimal("100.00"))


class GetOrCreateCartTest(TestCase):
    def setUp(self):
        self.user = AppUser.objects.create_user(
            email="test@example.com",
            password="testpass123",
        )

    def test_creates_pending_order_if_none_exists(self):
        order = get_or_create_cart(self.user)
        self.assertEqual(order.status, "pending")
        self.assertEqual(order.customer, self.user)

    def test_returns_existing_pending_order(self):
        existing = Order.objects.create(
            customer=self.user,
            status="pending",
            total_amount=Decimal("0.00"),
        )
        order = get_or_create_cart(self.user)
        self.assertEqual(order.id, existing.id)

    def test_does_not_return_confirmed_order(self):
        Order.objects.create(
            customer=self.user,
            status="confirmed",
            total_amount=Decimal("50.00"),
        )
        order = get_or_create_cart(self.user)
        self.assertEqual(order.status, "pending")


class AddToCartViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = AppUser.objects.create_user(
            email="test@example.com",
            password="testpass123",
        )
        self.garment, self.product = create_test_garment()

    def test_anonymous_user_add_to_session_cart(self):
        response = self.client.post(
            reverse("add-to-cart", kwargs={"garment_id": self.garment.id}),
            {
                "color": self.product.color.id,
                "size": self.product.size.id,
            }
        )
        self.assertEqual(response.status_code, 200)
        cart = self.client.session.get("cart", {})
        self.assertIn(str(self.product.id), cart)

    def test_authenticated_user_add_to_db_cart(self):
        self.client.login(username="test@example.com", password="testpass123")
        response = self.client.post(
            reverse("add-to-cart", kwargs={"garment_id": self.garment.id}),
            {
                "color": self.product.color.id,
                "size": self.product.size.id,
            }
        )
        self.assertEqual(response.status_code, 200)
        order = Order.objects.filter(customer=self.user, status="pending").first()
        self.assertIsNotNone(order)
        self.assertTrue(order.items.filter(product=self.product).exists())

    def test_out_of_stock_returns_error(self):
        self.product.stock = 0
        self.product.save()
        response = self.client.post(
            reverse("add-to-cart", kwargs={"garment_id": self.garment.id}),
            {
                "color": self.product.color.id,
                "size": self.product.size.id,
            }
        )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn("error", data)

    def test_auto_select_single_color_and_size(self):
        self.client.login(username="test@example.com", password="testpass123")
        response = self.client.post(
            reverse("add-to-cart", kwargs={"garment_id": self.garment.id}),
            {}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get("success"))


class CheckoutViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = AppUser.objects.create_user(
            email="test@example.com",
            password="testpass123",
        )
        self.customer = create_complete_customer(self.user)
        self.garment, self.product = create_test_garment()
        self.client.login(username="test@example.com", password="testpass123")

        self.order = get_or_create_cart(self.user)
        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
            unit_price=self.product.garment.price,
        )
        update_order_total(self.order)

    def test_checkout_confirms_order(self):
        response = self.client.post(reverse("checkout"), {
            "payment_type": "pod",
        })
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, "confirmed")

    def test_checkout_decrements_stock(self):
        initial_stock = self.product.stock
        self.client.post(reverse("checkout"), {"payment_type": "pod"})
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, initial_stock - 1)

    def test_checkout_redirects_to_success(self):
        response = self.client.post(reverse("checkout"), {"payment_type": "pod"})
        self.assertRedirects(response, reverse("order-completed"))

    def test_checkout_blocked_if_profile_incomplete(self):
        self.customer.first_name = ""
        self.customer.save()
        response = self.client.post(reverse("checkout"), {"payment_type": "pod"})
        self.assertRedirects(response, reverse("cart"))
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, "pending")

    def test_checkout_blocked_if_cart_empty(self):
        self.order.items.all().delete()
        response = self.client.post(reverse("checkout"), {"payment_type": "pod"})
        self.assertRedirects(response, reverse("cart"))

    def test_checkout_blocked_if_insufficient_stock(self):
        self.product.stock = 0
        self.product.save()
        response = self.client.post(reverse("checkout"), {"payment_type": "pod"})
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, "pending")

    def test_checkout_awards_loyalty_points(self):
        initial_points = self.user.loyalty_points
        self.client.post(reverse("checkout"), {"payment_type": "pod"})
        self.user.refresh_from_db()
        self.assertGreater(self.user.loyalty_points, initial_points)

    def test_unauthenticated_checkout_redirects_to_login(self):
        self.client.logout()
        response = self.client.post(reverse("checkout"), {"payment_type": "pod"})
        self.user.refresh_from_db()
        self.assertRedirects(response, reverse("login"))


class MergeSessionCartTest(TestCase):
    def setUp(self):
        self.user = AppUser.objects.create_user(
            email="merge@example.com",
            password="testpass123",
        )
        category = Category.objects.create(name="Tops", slug="tops")
        color = Color.objects.create(name="Green", hex_code="#00ff00")
        size = Size.objects.create(name="L")
        self.garment = Garment.objects.create(
            name="Green Top",
            slug="green-top",
            price=Decimal("30.00"),
        )
        self.garment.category.add(category)
        self.product = Product.objects.create(
            garment=self.garment,
            color=color,
            size=size,
            stock=10,
        )

    def test_session_cart_merges_on_login(self):
        session = self.client.session
        session["cart"] = {str(self.product.id): 2}
        session.save()

        self.client.post(reverse("login"), {
            "username": "merge@example.com",
            "password": "testpass123",
        })

        order = get_or_create_cart(self.user)
        item = order.items.filter(product=self.product).first()
        self.assertIsNotNone(item)
        self.assertEqual(item.quantity, 2)

    def test_session_cart_cleared_after_login(self):
        session = self.client.session
        session["cart"] = {str(self.product.id): 1}
        session.save()

        self.client.post(reverse("login"), {
            "username": "merge@example.com",
            "password": "testpass123",
        })

        self.assertNotIn("cart", self.client.session)

    def test_empty_session_cart_does_nothing(self):
        self.client.post(reverse("login"), {
            "username": "merge@example.com",
            "password": "testpass123",
        })

        order = Order.objects.filter(
            customer=self.user,
            status="pending"
        ).first()
        self.assertIsNone(order)

    def test_merge_increments_existing_db_item(self):
        order = get_or_create_cart(self.user)
        OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=1,
            unit_price=self.product.garment.price,
        )

        # Session has 3 more of the same product
        session = self.client.session
        session["cart"] = {str(self.product.id): 3}
        session.save()

        self.client.post(reverse("login"), {
            "username": "merge@example.com",
            "password": "testpass123",
        })

        order.refresh_from_db()
        item = order.items.filter(product=self.product).first()
        self.assertEqual(item.quantity, 4)