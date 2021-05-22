from django.contrib.auth.models import User
from playlists.models import Event, Playlist
from json import dumps


def get_recent_events(limit: int = 50, offset: int = 0, user: User = None, verified=True):
    if verified:
        events = Event.objects.filter(is_verified=True)
    else:
        events = Event.objects
    return events.order_by('starts_at')[offset: offset + limit]


def get_event_if_available(user: User, event_id: int):
    event_list = Event.objects.filter(id=event_id)
    if len(event_list):
        event = event_list[0]
        return event
    return None


def get_playlist_if_available(user: User, playlist_id: int):
    playlist_list = Playlist.objects.filter(id=playlist_id)
    if len(playlist_list):
        playlist = playlist_list[0]
        if not playlist.hidden or playlist.creator == user:
            return playlist
    return None


def time_to_laps(race_time, lap_time):
    m, s = [int(i) for i in lap_time.split(':')]
    lap_time = int(60 * m + s)
    race_time = int(race_time) * 60
    return int(race_time / lap_time)


def fuel_calculator(total_laps, fuel_per_lap):
    minfuel = int(total_laps) * float(fuel_per_lap) + float(fuel_per_lap)
    recfuel = int(total_laps) * float(fuel_per_lap) + float(fuel_per_lap) * 2 + 2
    return total_laps, int(minfuel), int(recfuel)
