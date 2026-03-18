from django.apps import AppConfig


class OrdersConfig(AppConfig):
    name = 'fashionWebsite.orders'

    def ready(self):
        import fashionWebsite.orders.signals
