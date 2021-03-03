from django.contrib.admin import register
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.contrib import messages
from django.core.validators import validate_email
from . import serializers

# Create your views here.

from authorization.forms import LoggingInForm, RegistrationForm
from .serializers import RegisterSerializer


def index(request):
    content = dict()
    content['user'] = request.user
    if request.method == "POST":
        post = request.POST
        if 'logout' in post:
            logout(request)
    return render(request, 'pages/index.html', content)

def check_Anonymous(user):
    if not user.is_anonymous:
        return user
    else:
        return None

def log_in(request):
    content = dict()
    register()
    content['login_form'] = LoggingInForm()
    content['register_form'] = RegistrationForm()
    content['user'] = request.user
    if request.method == "POST":
        post = request.POST
        if 'logout' in post:
            logout(request)
        elif 'logging' in post:
            form = LoggingInForm(request.POST)
            user = authenticate(username=form.data['username'], password=form.data['password'])
            if user is not None:
                login(request, user)
                content['authorized'] = True
                content['user'] = user
                content['login_form'] = form
            else:
                messages.add_message(request, messages.WARNING, f'Incorrect username or password')
        elif 'register' in post:
            form = RegistrationForm(request.POST)
            if form.is_valid():
                username = form.data['username']
                if not User.objects.filter(username=username).exists():
                    serializer = RegisterSerializer.create(RegisterSerializer(), form.data)
                    for elem in form.data:
                        print(elem)
                    user = serializer.save()
                else:
                    messages.add_message(request, messages.ERROR, f'This username is already taken: {username}')
            else:
                output_fields = list()
                for a in RegistrationForm().base_fields:
                    output_fields.append(a)
                for elem in form.data:
                    if len(form.data[elem]) == 0 and elem != 'register':
                        messages.add_message(request, messages.ERROR, f'The {elem} field is not correct')
                    elif elem == 'email':
                        try:
                            validate_email(form.data[elem])
                        except Exception as e:
                            messages.add_message(request, messages.ERROR, str(e.args[0]))
                    if elem != 'csrfmiddlewaretoken':
                        output_fields.remove(str(elem))
                for field in output_fields:
                    messages.add_message(request, messages.ERROR, f'The {field} field is not correct')
            content['register_form'] = form
        content['request'] = request
        content['user'] = check_Anonymous(request.user)
        return render(request, 'pages/login.html', content)
    elif request.method == "GET":
        content['request'] = request
        content['user'] = check_Anonymous(request.user)
        return render(request, 'pages/login.html', content)
