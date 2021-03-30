from .views import event, get_events, create_playlist, get_playlist
from django.urls import path

urlpatterns = [
    path('eventlist/', get_events),
    path('event/<int:event_id>', event),
    path('playlist/create', create_playlist),
    path('playlist/<int:playlist_id>', get_playlist)
]