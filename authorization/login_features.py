from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

from authorization.models import Stats
from authorization.serializers import RegisterSerializer, StatsSerializer


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
    else:
        messages.add_message(request, messages.ERROR, f'This username is already taken: {username}')


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
