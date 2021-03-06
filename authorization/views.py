from django.contrib.admin import register
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.contrib import messages
from django.core.validators import validate_email
from . import serializers
# Create your views here.

from authorization.forms import LoggingInForm, RegistrationForm
from .login_features import check_anonymous, register_proj, login_proj


def index(request):
    content = dict()
    content['user'] = request.user
    if request.method == "POST":
        post = request.POST
        if 'logout' in post:
            logout(request)
    return render(request, 'pages/index.html', content)


def log_in(request):
    content = {'login_form': LoggingInForm(), 'register_form': RegistrationForm(), 'user': request.user}
    if request.method == "POST":
        post = request.POST
        if 'logout' in post:
            logout(request)

        elif 'logging' in post:
            form = LoggingInForm(request.POST)
            user = authenticate(username=form.data['username'], password=form.data['password'])
            content = login_proj(user, request, content, form)

        elif 'register' in post:
            form = RegistrationForm(request.POST)
            if form.is_valid():
                username = form.data['username']
                register_proj(username, request, content, form)
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

    content.update({'request': request, 'user': check_anonymous(request.user)})
    return render(request, 'pages/login.html', content)
