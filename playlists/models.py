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
        ('Multi', 'Multi'),
        ('Cup', 'Cup'),
        ('ST', 'ST'),
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

    LICENSE = (
        ('Overall', 0),
        ('ProAm', 1),
        ('Am', 2),
        ('Silver', 3),
        ('National', 4),
    )
    EVENT_TYPE = (
        ('Single', 'Single'),
        ('Command', 'Command'),
    )
    RACE_TYPE = (
        ('Single race', 'Single race'),
        ('Championship', 'Championship'),
    )
    CAR_CLASS_CHOICES = (
        ('GT3', 'GT3'),
        ('GT4', 'GT4'),
        ('Multi', 'Multi'),
        ('Cup', 'Cup'),
        ('ST', 'ST'),
    )
    EVENT_LICENSE = (
        ('All', 'All'),
        ('Club', 'Club'),
    )
    QUALIFY_TYPE = (
        ('Fastest lap', 'Fastest lap'),
        ('Average lap', 'Average lap'),
    )
    GRID_CHOICES = (
        ('Main', 'Main'),
        ('Reversed', 'Reversed')
    )
    name = CharField(max_length=255)
    track = CharField(max_length=50)
    icon = CharField(max_length=100)
    description = TextField()
    starts_at = DateTimeField()
    event_type = CharField(max_length=15, choices=EVENT_TYPE)
    race_type = CharField(max_length=15, choices=RACE_TYPE)
    car_class = CharField(max_length=5, choices=CAR_CLASS_CHOICES)
    license = CharField(max_length=15, choices=EVENT_LICENSE)
    pilots_in_command = IntegerField()
    tyre_sets = IntegerField()
    mandatory_pits = IntegerField()
    quali_type = CharField(max_length=30, choices=QUALIFY_TYPE)
    grid_type = CharField(max_length=15, choices=GRID_CHOICES)
    pit_window = CharField(max_length=30)
    penalty_sys = BooleanField(default=True)
    is_verified = BooleanField(default=False)


class CarClass(models.Model):

    name = CharField(max_length=30)


class Car(models.Model):

    name = CharField(max_length=255)
    type = ForeignKey(CarClass, on_delete=models.deletion.RESTRICT)


class Registration(models.Model):

    event = ForeignKey(Event, on_delete=models.deletion.CASCADE)
    user = ForeignKey(User, on_delete=models.deletion.CASCADE)
    car = ForeignKey(Car, on_delete=models.deletion.CASCADE)
    preferred_number = IntegerField()
