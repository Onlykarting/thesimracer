from playlists.models import Event, Registration
from django.contrib.auth.models import User


def user_registered_on_event(event: Event, user: User) -> bool:
    return Registration.objects.filter(event_id=event.id, user_id=user.id).exists()
