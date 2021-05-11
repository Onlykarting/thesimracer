from io import BytesIO
from playlists.models import Playlist, Event
from django.contrib.auth.models import User
from playlists.services.exceptions import PermissionDenied
from typing import Optional


def save_playlist_thumbnail(thumbnail) -> str:
    """
    Saves given thumbnail and returns path to a file.
    :param thumbnail: a file that needs to be saved
    :return: str, path to the saved file
    """
    pass


def create_playlist(creator: User, name: str, description: str = "", thumbnail: str = "",
                    verified: bool = False, pilot_qualify: str = "AM", playlist_type: str = "solo") -> Playlist:
    """
    Creates team playlist
    :param playlist_type:
    :param pilot_qualify:
    :param verified:
    :param creator:
    :param name:
    :param description:
    :param thumbnail:
    :return: created playlist
    """
    playlist = Playlist(name=name, description=description, thumbnail=thumbnail, pilot_qualify=pilot_qualify,
                        is_verified=verified, creator=creator, type=playlist_type)
    playlist.save()
    return playlist


def is_playlist_creator(user: User) -> bool:
    """
    Checks if user is playlist creator.
    :param user:
    :return: True if user is playlist creator, else False
    """
    return Playlist.objects.filter(creator=user).exists()


def add_event_to_playlist(playlist: Playlist, event: Event, user: User):
    """
    Adds sole event to playlist and checks user's permission for this operation.
    Raises PermissionDenied if user is not allowed to add event to playlist.
    Raises ValueError if event is already in playlist, event type and playlist type aren't same.
    Because adding events to published playlists are not allowed also raises ValueError
    :param playlist: playlist
    :param event: event
    :param user: user
    :return: None
    """
    if playlist.type != event.type:
        raise ValueError("Playlist type and event type must be equal. Got {} and {}".format(playlist.type, event.type))

    if event in playlist.event_set:
        raise ValueError("Event is already in playlist.")

    if playlist.creator != user:
        raise PermissionDenied("User must be playlist creator.")

    if not playlist.hidden:
        raise ValueError("Playlist event has been already published and can't be edited anymore.")

    event.playlist = playlist
    event.save()


def remove_event_from_playlist(playlist: Playlist, event: Event, user: User):

    if playlist.creator != user:
        raise PermissionDenied("User must be playlist creator.")

    if event not in playlist.event_set:
        raise ValueError("Event is not in playlist.")

    if not playlist.hidden:
        raise ValueError("Playlist event has been already published and can't be edited anymore.")

    event.playlist = None
    event.save()


