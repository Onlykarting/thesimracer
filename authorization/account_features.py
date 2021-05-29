import json

import requests
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import redirect

from authorization.models import Stats, Countries
from authorization.serializers import RegisterSerializer, StatsSerializer
import re

def check_anonymous(user):
    if not user.is_anonymous:
        return user
    else:
        return None


def register_proj(username, request, content, form):
    if not User.objects.filter(username=username).exists():
        serializer = RegisterSerializer.create(RegisterSerializer(), form.data)
        user = serializer.save()
        user = authenticate(username=form.data['username'], password=form.data['password'])
        login_proj(user, request, content, form)
        return True
    else:
        messages.add_message(request, messages.ERROR, f'This username is already taken: {username}')
        return False


def login_proj(user, request, content, form):
    if user is not None:
        login(request, user)
        content.update({'authorized': True, 'user': user, 'login_form': form})
    else:
        messages.add_message(request, messages.WARNING, f'Incorrect username or password')
        content.update({'user': user, 'login_form': form})
    return content


def set_stats(user, country_flag=None):
    if country_flag is not None:
        Stats.objects.filter(user=user).delete()
        stats = Stats(user=user, country_flag=country_flag)
    else:
        stats = Stats(user=user)
    stats.save()


def update_stats(user, post):
    user_cur = User.objects.get(id=user.id)
    user_cur.first_name = post['first_name']
    user_cur.last_name = post['last_name']
    user_cur.save()
    country = Countries.objects.get(country_name=post['country_name'])
    stats = Stats.objects.get(user_id=user.id)
    stats.discord, stats.twitch, stats.instagram, stats.description, stats.tag, stats.country = post['discord'], post['twitch'], post['instagram'],\
    post['description'], post['tag'].upper(), country
    stats.save()


def validate_names(string):
    for el in string:
        if not bool(re.match("""[a-zA-Zа-яА-Я]""", el)):
            return False
    return True


def check_names(form):
    first_name = form['first_name']
    last_name = form['last_name']
    if validate_names(first_name) and validate_names(last_name):
        return True
    else:
        return False


def profile_load(request, user):
    if request.user.username == user:
        owner = True
    else:
        owner = False
    person = User.objects.get(username=user)
    id = person.id
    first_name = person.first_name
    last_name = person.last_name
    stats = Stats.objects.get(user_id=id)
    country = stats.country
    ip = request.META.get('REMOTE_ADDR')
    response = requests.get('http://ipwhois.app/json/' + ip)
    respose_dict = json.loads(response.content.decode("UTF-8"))
    country_flag = respose_dict['country_flag']
    return {'stats': stats, 'first_name': first_name, 'last_name': last_name, 'country_flag': country_flag, 'country': country, 'owner': owner, 'id': id}