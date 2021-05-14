from .services import get_recent_events, get_event_if_available, get_playlist_if_available
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.views.defaults import page_not_found, bad_request, permission_denied
from .forms import PlaylistCreationForm


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



def get_results(request):
    return render(request, 'results.html', {})


def create_report(request):
    return render(request, 'report-create.html', {})


def reports(request):
    return render(request, 'reports.html', {})


def tools(request):
    return render(request, 'tools.html', {})


def event(request, event_id: int):
    event_ = get_event_if_available(request.user, event_id)
    if event_ is None:
        return page_not_found(request, '')
    context = {
        "event": event_,
        "user": request.user,
        "is_authenticated": request.user.is_authenticated,
        "event_id": event_id,
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


@login_required(login_url='/login')
def register_on_event(request, event_id: int):
    event = get_event_if_available(request.user, event_id)
    if event:
        if not event.registered_users.filter(username=request.user.username).exists():
            return render(request, 'event-register.html', {})
        else:
            return permission_denied(request, '')
    else:
        return page_not_found(request, '')


@login_required(login_url='/login')
def unregister_on_event(request, event_id: int):
    event = get_event_if_available(request.user, event_id)
    if event:
        if event.registered_users.filter(username=request.user.username).exists():
            event.registered_users.remove(request.user)
            return redirect(f'/event/{event_id}')
        else:
            return permission_denied(request, '')
    else:
        return page_not_found(request, '')


def get_playlists(request):
    return render(request, 'championships.html', {})


def get_playlist_races(request, playlist_id: int):
    return render(request, 'championship-events.html', {})


def register_on_playlist(request, playlist_id: int):
    playlist = get_playlist_if_available(request.user, playlist_id)
    if playlist:
        return render(request, 'championship-register.html', {})
    else:
        return page_not_found(request, '')


@login_required(login_url='/login')
def create_playlist(request):
    if request.method == 'GET':
        return render(request, 'create-playlist.html', {})
    elif request.method == 'POST':
        form_data = {
            'name': request.POST.get('name', ''),
            'description': request.POST.get('description', ''),
            'creator': request.user,
            'thumbnail': request.FILES.get('thumbnail'),
            'pilot_qualify': request.POST.get('pilot_qualify', 'AM'),
            'grid_type': request.POST.get('grid_type', 'Main'),
            'qualify_type': request.POST.get('qualify_type', 'Average'),
            'car_class': request.POST.get('car_class', 'Multi'),
            'tyre_sets_count': request.POST.get('tyre_sets_count', 50),
            'pilot_count': request.POST.get('pilot_count', 1),
            'mandatory_pit_stop_count': request.POST.get('mandatory_pit_stop_count', 1)
        }
        form = PlaylistCreationForm(form_data)
        if form.is_valid():
            instance = form.save()
    return bad_request(request, '')