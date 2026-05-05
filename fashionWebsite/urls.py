from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include("fashionWebsite.common.urls")),
    path('admin/', admin.site.urls),
    path('accounts/', include("fashionWebsite.accounts.urls")),
    path('clothes/', include("fashionWebsite.clothes.urls")),
    path('orders/', include("fashionWebsite.orders.urls")),
    path('accounts/', include('allauth.urls')),
    path("reviews/", include("fashionWebsite.reviews.urls")),
    path("i18n/", include("django.conf.urls.i18n")),
]

urlpatterns += i18n_patterns(
    path('', include("fashionWebsite.common.urls")),
    path('accounts/', include("fashionWebsite.accounts.urls")),
    path('clothes/', include("fashionWebsite.clothes.urls")),
    path('orders/', include("fashionWebsite.orders.urls")),
    path('accounts/', include('allauth.urls')),
    path("reviews/", include("fashionWebsite.reviews.urls")),
    path("i18n/", include("django.conf.urls.i18n")),
)

if settings.DEBUG:
    urlpatterns += [
        path('rosetta/', include('rosetta.urls')),
    ]

