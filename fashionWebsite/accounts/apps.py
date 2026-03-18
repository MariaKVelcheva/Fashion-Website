from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'fashionWebsite.accounts'

    def ready(self):
        import fashionWebsite.accounts.signals
