from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include("fashionWebsite.common.urls")),
    path('admin/', admin.site.urls),
    path('accounts/', include("fashionWebsite.accounts.urls")),
    path('clothes/', include("fashionWebsite.clothes.urls")),
]
