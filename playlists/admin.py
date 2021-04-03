from django.contrib import admin
from playlists.models import Playlist, Event, AccEvent


class EventAdmin(admin.ModelAdmin):
    pass


class PlaylistAdmin(admin.ModelAdmin):
    pass


class AccEventAdmin(admin.ModelAdmin):
    pass


admin.site.register(Event, EventAdmin)
admin.site.register(Playlist, PlaylistAdmin)
