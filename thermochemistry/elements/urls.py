"""URL config for Elements."""
from django.urls import path

from .views import ElementsDetailView, ElementsListView

app_name = 'elements'

urlpatterns = [
    path(
        'list/',
        ElementsListView.as_view(),
        name='list'
    ),
    path(
        'elements/<int:pk>/',
        ElementsDetailView.as_view(),
        name='detail'
    ),
]
