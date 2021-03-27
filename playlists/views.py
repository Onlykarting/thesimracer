from .services import get_recent_events, get_event_if_available
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def get_events(request):
    limit = request.GET.get('limit', 0)
    offset = request.GET.get('offset', 0)
    events = get_recent_events(limit, offset, request.user)
    context = {
        'events': events,
        'events_on_page': 10,
        'is_authenticated': request.user.is_authenticated,
        'user':  request.user,
        'limit': limit,
        'offset': offset
    }
    return render(request, 'events.html', context)


def event(request, event_id: int):
    event_ = get_event_if_available(request.user, event_id)
    context = {
        "ok": event_ is not None,
        "event": event_,
        "user": request.user,
        "is_authenticated": request.user.is_authenticated,
    }
    return render(request, 'event.html', context)
