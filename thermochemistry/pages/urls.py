"""URL config for pages."""
from django.urls import path

from .views import HomeTemplateView, AboutTemplateView

app_name = 'pages'

urlpatterns = [
    path('', HomeTemplateView.as_view(), name='home'),
    path('about/', AboutTemplateView.as_view(), name='about'),
]
