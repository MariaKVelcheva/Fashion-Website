from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("fashionWebsite.accounts.urls")),
    path('clothes/', include("fashionWebsite.clothes.urls")),
    path('', include("fashionWebsite.common.urls")),
]
