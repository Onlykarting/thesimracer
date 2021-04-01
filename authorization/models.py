from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Stats(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    races = models.IntegerField(default=0)
    bestlaps = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    poles = models.IntegerField(default=0)
    img = models.ImageField(upload_to='avatars', default='static/images/avatar.jpg')