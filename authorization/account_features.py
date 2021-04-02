from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

from authorization.models import Stats
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


def set_stats(user):
    stats = Stats(user=user)
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