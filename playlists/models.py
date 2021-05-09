from acc_server.models import AccEvent
from django.db import models
from django.db.models import CharField, BooleanField, TextField, DateTimeField, ForeignKey, OneToOneField, ImageField, IntegerField, ManyToManyField
from django.contrib.auth.models import User


class Playlist(models.Model):

    PILOT_QUALIFY_CHOICES = (

        ('AM', 'AM'),
        ('SILVER', 'SILVER') ,
        ('PRO-AM', 'PRO-AM'),
        ('PRO', 'PRO')
    )
    GRID_CHOICES = (
        ('Main', 'Main'),
        ('Reversed', 'Reversed')
    )
    QUALIFY_TYPE_CHOICES = (
        ('Fastest', 'Fastest'),
        ('Average', 'Average')
    )
    CAR_CLASS_CHOICES = (
        ('GT3', 'GT3'),
        ('GT4', 'GT4'),
        ('Multi', 'Multi')
    )

    creator = ForeignKey(User, models.deletion.CASCADE)
    name = CharField(max_length=255)
    description = TextField(default='')
    hidden = BooleanField(default=True)
    thumbnail = ImageField(upload_to='thumbs', null=True)
    pilot_qualify = CharField(max_length=255, choices=PILOT_QUALIFY_CHOICES)
    grid_type = CharField(max_length=255, choices=GRID_CHOICES)
    qualify_type = CharField(max_length=255, choices=QUALIFY_TYPE_CHOICES)
    car_class = CharField(max_length=255, choices=CAR_CLASS_CHOICES)
    tyre_sets_count = IntegerField()
    pilot_count = IntegerField()
    mandatory_pit_stop_count = IntegerField()


class Event(models.Model):

    playlist = ForeignKey(Playlist, on_delete=models.deletion.CASCADE, null=True)
    game_settings = OneToOneField(AccEvent, on_delete=models.deletion.CASCADE)
    name = CharField(max_length=255)
    description = TextField()
    starts_at = DateTimeField()
    registration_starts_at = DateTimeField()
    registration_ends_at = DateTimeField()
    is_verified = BooleanField(default=False)


class CarClass(models.Model):

    name = CharField(max_length=30)


class Car(models.Model):

    name = CharField(max_length=255)
    type = ForeignKey(CarClass, on_delete=models.deletion.RESTRICT)


class Team(models.Model):

    name = CharField(max_length=255)
    host = ForeignKey(User, on_delete=models.deletion.RESTRICT, related_name='team_host')
    members = ManyToManyField(User, related_name='team_members')


class Registration(models.Model):

    event = ForeignKey(Event, on_delete=models.deletion.CASCADE)
    user = ForeignKey(User, on_delete=models.deletion.CASCADE)
    team = ForeignKey(Team, on_delete=models.deletion.SET_NULL, null=True)
    car = ForeignKey(Car, on_delete=models.deletion.CASCADE)
    preferred_number = IntegerField()
