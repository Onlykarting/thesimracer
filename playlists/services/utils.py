from django.contrib.auth.models import User
from playlists.models import Event, Playlist
from json import dumps


def get_recent_events(limit: int = 50, offset: int = 0, user: User = None):
    events = Event.objects.order_by('starts_at')[offset: offset + limit]
    return events


def get_event_if_available(user: User, event_id: int):
    event_list = Event.objects.filter(id=event_id)
    event__ = [entry for entry in event_list.values()]
    if len(event__) > 0:
        event__ = event__[0]
    if len(event__) != 0:
        event = event__
        if user.is_authenticated:
            return event
        else:
            return event
    return None


def get_playlist_if_available(user: User, playlist_id: int):
    playlist_list = Playlist.objects.filter(id=playlist_id)
    if len(playlist_list):
        playlist = playlist_list[0]
        if not playlist.hidden or playlist.creator == user:
            return playlist
    return None