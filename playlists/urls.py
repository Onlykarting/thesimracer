from .views import event, get_events, create_playlist, get_playlist, get_results, indev
from django.urls import path

urlpatterns = [
    path('eventlist/', get_events),
    path('resultlist/', get_results),
    path('tools/', indev),
    path('reports/', indev),
    path('support/', indev),
    path('stats/', indev),
    path('help-us/', indev),
    path('event/<int:event_id>', event),
    path('playlist/create', create_playlist),
    path('playlist/<int:playlist_id>', get_playlist)
]