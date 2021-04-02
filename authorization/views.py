import json
from django.contrib.admin import register
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.validators import validate_email
from . import serializers
# Create your views here.

from authorization.forms import LoggingInForm, RegistrationForm
from .account_features import check_anonymous, register_proj, login_proj, set_stats, check_names
from .models import Stats
import requests

def index(request):
    content = dict()
    content['user'] = request.user
    if request.method == "POST":
        post = request.POST
        if 'logout' in post:
            logout(request)
    return render(request, 'pages/index.html', content)


def log_in(request):
    content = {'login_form': LoggingInForm(), 'register_form': RegistrationForm(), 'user': request.user, 'register_page': False}
    if request.method == "POST":
        post = request.POST
        if 'logout' in post:
            logout(request)
        elif 'logging' in post:
            form = LoggingInForm(request.POST)
            user = authenticate(username=form.data['username'], password=form.data['password'])
            content = login_proj(user, request, content, form)
        elif 'register' in post:
            content['register_page'] = True
            form = RegistrationForm(request.POST)
            if form.is_valid():
                if check_names(form.data):
                    username = form.data['username']
                    if register_proj(username, request, content, form):
                        set_stats(request.user)
                        print(request.user)
                else:
                    messages.add_message(request, messages.ERROR, 'First name or last name is not correct.')
            else:
                output_fields = list()
                for a in RegistrationForm().base_fields:
                    output_fields.append(a)
                for elem in form.data:
                    if len(form.data[elem]) == 0 and elem != 'register':
                        messages.add_message(request, messages.ERROR, f'The {elem} field is not correct')
                        print(elem)
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
    elif request.method == 'GET':
        if 'register' in request.GET:
            content['register_page'] = True
    content.update({'request': request, 'user': check_anonymous(request.user)})
    return render(request, 'pages/login.html', content)


def profile(request):
    content = {'user': check_anonymous(request.user)}
    if request.method == "GET":
        if request.user.is_authenticated:
            username = request.user
            user = User.objects.get(id=username.id)
            first_name = user.first_name
            last_name = user.last_name
            stats = Stats.objects.get(user=username)
            ip = request.META.get('REMOTE_ADDR')
            response = requests.get('http://ipwhois.app/json/' + ip)
            respose_dict = json.loads(response.content.decode("UTF-8"))
            country_flag = respose_dict['country_flag']
            content.update({'stats': stats, 'first_name': first_name, 'last_name': last_name, 'country_flag': country_flag})
    if request.method == "POST":
        if 'logout' in request.POST:
            logout(request)
            return redirect('/')
    return render(request, 'pages/profile.html', content)