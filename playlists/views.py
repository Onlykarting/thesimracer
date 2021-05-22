from .services import get_recent_events, get_event_if_available, get_playlist_if_available, \
    time_to_laps, fuel_calculator
from .services.events import user_registered_on_event
from .models import Registration, Car, CarClass
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.views.defaults import page_not_found, bad_request, permission_denied
from .forms import PlaylistCreationForm
from django.utils import timezone
from datetime import datetime
from playlists.models import Event, AccEvent


def get_events(request, sort='official'):
    limit = request.GET.get('limit', 10)
    offset = request.GET.get('offset', 0)
    verified = {
        'official': True,
        'all': False
    }
    events = get_recent_events(limit, offset, request.user, verified[sort])
    context = {
        'events': events,
        'events_on_page': 10,
        'is_authenticated': request.user.is_authenticated,
        'user':  request.user,
        'limit': limit,
        'offset': offset
    }
    return render(request, 'events.html', context)


def indev(request):
    return render(request, 'in-development.html', {})


def about_us(request):
    return render(request, 'about-us.html', {})


def get_results(request):
    return render(request, 'results.html', {})


def create_report(request):
    return render(request, 'report-create.html', {})


def reports(request):
    return render(request, 'reports.html', {})


def tools(request):
    context = {}
    get = request.GET
    if 'race-time' in get:
        res = fuel_calculator(time_to_laps(get['race-time'], get['lap-time']), get['fuel'])
        context['total_laps'], context['min_fuel'], context['rec_fuel'] = res
    elif 'race-laps' in get:
        context['laps_tab'] = True
        res = fuel_calculator(get['race-laps'], get['fuel'])
        context['total_laps'], context['min_fuel'], context['rec_fuel'] = res
    return render(request, 'tools.html', context)


def event(request, event_id: int):
    event_ = get_event_if_available(request.user, event_id)
    if event_ is None:
        return page_not_found(request, '')
    context = {
        "event": event_,
        "user": request.user,
        "is_authenticated": request.user.is_authenticated,
        "event_id": event_id,
        "is_user_registered": user_registered_on_event(event_, request.user)
    }
    return render(request, 'event-page.html', context)


def get_playlist(request, playlist_id: int):
    playlist = get_playlist_if_available(request.user, playlist_id)
    if playlist:
        return render(request, 'championship-page.html', {
            'playlist': playlist,
            'playlist_events': playlist.event_set.all(),
            'playlist_id': playlist_id
        })
    else:
        return page_not_found(request, '')


@login_required(login_url='/login')
def create_event(request):
    if request.method == 'GET':
        return render(request, 'create-event.html', {})
    if request.method == 'POST':
        event_ = Event()
        event_.playlist = None
        event_.description = request.POST.get('description')
        event_.name = request.POST.get('name')
        start_datetime = f"{request.POST.get('event-date')} - {request.POST.get('event-time')}"
        event_.starts_at = datetime.strptime(start_datetime, '%Y-%m-%d - %H:%M')
        event_.game_settings = AccEvent()
        event_.game_settings.save()
        # event_.game_settings.event_settings.track
        event_.game_settings.event_rules.max_drivers_count = int(request.POST.get('pilot-count', 8))
        event_.game_settings.event_rules.mandatory_pitstop_count = int(request.POST.get('mandatory-pit-stop-count', 0))
        event_.game_settings.event_rules.tyre_set_count = int(request.POST.get('tyre-sets', 50))
        event_.game_settings.server_settings.car_group = request.POST.get('car-group')
        event_.game_settings.event_rules.qualify_standing_type = int(request.POST.get('qualify-type'))
        event_.game_settings.server_settings.allow_auto_dq = int(request.POST.get('penalty-system', 0))
        event_.game_settings.server_settings.max_car_slots = int(request.POST.get('max-car-count', 30))



        event_.save()
        return redirect(f"/event/{event_.pk}")


@login_required(login_url='/login')
def register_on_event(request, event_id: int):
    """
    Для регистрации на ивент в POST запросе принимает три параметра:
    - car_class - INT, id класса группы из базы
    - car_number - INT, предпочитаемый норер машины
    - car_id - INT, id машины из базы
    :param request:
    :param event_id:
    :return:
    """
    event = get_event_if_available(request.user, event_id)
    if event:
        if not user_registered_on_event(event, request.user):
            if request.method == 'GET':
                return render(request, 'event-register.html', {
                    'car_list': Car.objects.all(),
                    'car_classes': CarClass.objects.all()
                })
            elif request.method == 'POST':
                car_number = int(request.POST.get('car_number', 1))
                car_id = int(request.POST.get('car_id', 1))
                car_class = int(request.POST.get('car_class', 1))
                reg = Registration()
                reg.user = request.user
                reg.car_id = car_id
                reg.preferred_number = car_number
                reg.event_id = event_id
                reg.save()
                return redirect(f"/event/{event_id}")
        else:
            return permission_denied(request, '')
    else:
        return page_not_found(request, '')


@login_required(login_url='/login')
def unregister_on_event(request, event_id: int):
    event = get_event_if_available(request.user, event_id)
    if event:
        if user_registered_on_event(event, request.user):
            Registration.objects.get(event_id=event_id, user_id=request.user.id).delete()
            return redirect(f"/event/{event_id}")
        else:
            return permission_denied(request, '')
    else:
        return page_not_found(request, '')


def get_playlists(request):
    return render(request, 'championships.html', {})
