from .views import event, get_events, create_playlist
from django.urls import path

urlpatterns = [
    path('', get_events),
    path('<int:event_id>', event),
    path('create', create_playlist)
]