from datetime import datetime, timezone
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Countries(models.Model):
    country_flag = models.CharField(max_length=65, default='/static/images/flags/DefaultFlag.bmp')
    country_name = models.CharField(default=0, max_length=25)


class Stats(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    races = models.IntegerField(default=0)
    bestlaps = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    poles = models.IntegerField(default=0)
    img = models.ImageField(upload_to='avatars', default='/static/images/Avatar.png')
    discord = models.CharField(default=0, max_length=20)
    twitch = models.CharField(default=0, max_length=20)
    instagram = models.CharField(default=0, max_length=20)
    description = models.TextField(default=0, max_length=500)
    tag = models.CharField(default=0, max_length=3)
    country_flag = models.CharField(default=0, max_length=40)
    steam_id = models.CharField(max_length=65, null=True)
    country = models.ForeignKey(to=Countries, on_delete=models.CASCADE, default=1)


