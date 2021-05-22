from .views import event, get_events, create_playlist, get_playlist, register_on_event, unregister_on_event, \
    create_event, get_results, indev, get_playlists, get_playlist_races, register_on_playlist, tools, create_report, reports, about_us
from django.urls import path

urlpatterns = [
    path('eventlist/<str:sort>', get_events),
    path('eventlist/', get_events),
    path('resultlist/', get_results),
    path('tools/', tools),
    path('report/create', create_report),
    path('reports/', reports),
    path('support/', indev),
    path('stats/', indev),
    path('help-us/', indev),
    path('about-us/', about_us),
    path('event/<int:event_id>', event),
    path('event/create/', create_event),
    path('event/<int:event_id>/register', register_on_event),
    path('event/<int:event_id>/unregister', unregister_on_event),
    path('championships', get_playlists),
    path('playlist/create', create_playlist),
    path('playlist/<int:playlist_id>', get_playlist),
    path('playlist/<int:playlist_id>/register', register_on_playlist),
    path('playlist/<int:playlist_id>/races', get_playlist_races)
]
