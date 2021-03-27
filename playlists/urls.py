from .views import event, get_events
from django.urls import path

urlpatterns = [
    path('', get_events),
    path('<int:event_id>', event)
]