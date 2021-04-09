from django.contrib import admin
from acc_server.models import AccEvent, Session, ServerConfig, ServerSettings, EventSettings, \
    EventRules, AssistRules, Track


class AccEventAdmin(admin.ModelAdmin):
    pass


class TrackAdmin(admin.ModelAdmin):
    pass


class SessionAdmin(admin.ModelAdmin):
    pass


class ServerConfigAdmin(admin.ModelAdmin):
    pass


class ServerSettingsAdmin(admin.ModelAdmin):
    pass


class ServerWorkerAdmin(admin.ModelAdmin):
    pass


class EventSettingsAdmin(admin.ModelAdmin):
    pass


class EventRulesAdmin(admin.ModelAdmin):
    pass


class AssistRulesAdmin(admin.ModelAdmin):
    pass


admin.site.register(Session, SessionAdmin)
admin.site.register(AccEvent, AccEventAdmin)
admin.site.register(ServerConfig, ServerConfigAdmin)
admin.site.register(ServerSettings, ServerSettingsAdmin)
admin.site.register(EventSettings, EventSettingsAdmin)
admin.site.register(EventRules, EventRulesAdmin)
admin.site.register(AssistRules, AssistRulesAdmin)
admin.site.register(Track, TrackAdmin)
