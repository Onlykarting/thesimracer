from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render

# Create your views here.
from authorization.forms import LoggingInForm


def index(request):
    content = dict()
    content['user'] = request.user
    print(f'Вы: {request.user}')
    if request.method == "POST":
        form = LoggingInForm(request.POST)
        post = request.POST
        if 'logout' in post:
            print('Вы вышли')
            logout(request)
        elif 'login' in form.data:
            user = authenticate(username=form.data['login'], password=form.data['password'])
            if user is not None:
                login(request, user)
                content['authorized'] = True
                content['user'] = user
        content['request'] = request
        content['form'] = form
        return render(request, 'pages/index.html', content)
    elif request.method == "GET":
        content['form'] = LoggingInForm()
        content['request'] = request
        return render(request, 'pages/index.html', content)