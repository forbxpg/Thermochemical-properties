"""URLConf."""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('pages.urls')),
    path('', include('elements.urls')),
    path('admin/', admin.site.urls),
]
