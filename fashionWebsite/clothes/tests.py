from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from fashionWebsite.clothes.models import Garment, Product, Color, Size, Category
from decimal import Decimal


class GarmentModelTest(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Dresses", slug="dresses")
        self.color = Color.objects.create(name="Blue", hex_code="#0000ff")
        self.size = Size.objects.create(name="S")
        self.garment = Garment.objects.create(
            name="Summer Dress",
            slug="summer-dress",
            price=Decimal("75.00"),
        )
        self.garment.category.add(category)

    def test_is_available_with_stock(self):
        Product.objects.create(
            garment=self.garment,
            color=self.color,
            size=self.size,
            stock=5,
        )
        self.assertTrue(self.garment.is_available)

    def test_is_available_without_stock(self):
        Product.objects.create(
            garment=self.garment,
            color=self.color,
            size=self.size,
            stock=0,
        )
        self.assertFalse(self.garment.is_available)

    def test_is_new_within_60_days(self):
        self.garment.created_at = timezone.now() - timedelta(days=30)
        self.garment.save()
        self.assertTrue(self.garment.is_new)

    def test_is_new_outside_60_days(self):
        self.garment.created_at = timezone.now() - timedelta(days=61)
        self.garment.save()
        self.assertFalse(self.garment.is_new)

    def test_slug_auto_generated(self):
        garment = Garment.objects.create(
            name="Autumn Coat",
            price=Decimal("120.00"),
        )
        self.assertEqual(garment.slug, "autumn-coat")

    def test_get_available_colors(self):
        color2 = Color.objects.create(name="Red", hex_code="#ff0000")
        Product.objects.create(
            garment=self.garment, color=self.color,
            size=self.size, stock=5,
        )
        Product.objects.create(
            garment=self.garment, color=color2,
            size=self.size, stock=3,
        )
        colors = self.garment.get_available_colors()
        self.assertEqual(len(colors), 2)
