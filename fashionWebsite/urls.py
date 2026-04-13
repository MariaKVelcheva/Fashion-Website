from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include("fashionWebsite.common.urls")),
    path('admin/', admin.site.urls),
    path('accounts/', include("fashionWebsite.accounts.urls")),
    path('clothes/', include("fashionWebsite.clothes.urls")),
    path('orders/', include("fashionWebsite.orders.urls")),
    path('accounts/', include('allauth.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



