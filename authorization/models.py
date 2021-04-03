from datetime import datetime, timezone
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Stats(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    races = models.IntegerField(default=0)
    bestlaps = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    poles = models.IntegerField(default=0)
    img = models.ImageField(upload_to='avatars', default='/static/images/Avatar.png')
    discord = models.CharField(default=0, max_length=20)
    tag = models.CharField(default=0, max_length=3)
    country_flag = models.CharField(default=0, max_length=40)
