from acc_server.models import AccEvent
from django.db import models
from django.db.models import CharField, BooleanField, TextField, DateTimeField, ForeignKey, ManyToManyField, OneToOneField
from django.contrib.auth.models import User


class Playlist(models.Model):

    creator = ForeignKey(User, models.deletion.CASCADE)
    name = CharField(max_length=255)
    description = TextField()
    hidden = BooleanField()


class Event(models.Model):

    playlist = ForeignKey(Playlist, on_delete=models.deletion.CASCADE)
    game_settings = OneToOneField(AccEvent, on_delete=models.deletion.CASCADE)
    name = CharField(max_length=255)
    description = TextField()
    starts_at = DateTimeField()
    registration_starts_at = DateTimeField()
    registration_ends_at = DateTimeField()
