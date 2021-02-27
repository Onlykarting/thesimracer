from acc_server.models import ServerConfig, ServerSettings, AssistRules, EventRules, EventSettings
from rest_framework.serializers import ModelSerializer


class ServerConfigSerializer(ModelSerializer):
    class Meta:
        model = ServerConfig
        exclude = ["id"]
        read_only = True


class ServerSettingsSerializer(ModelSerializer):
    class Meta:
        model = ServerSettings
        exclude = ["id"]
        read_only = True


class AssistRulesSerializer(ModelSerializer):
    class Meta:
        model = AssistRules
        exclude = ["id"]
        read_only = True


class EventRulesSerializer(ModelSerializer):
    class Meta:
        model = EventRules
        exclude = ["id"]
        read_only = True


class EventSettingsSerializer(ModelSerializer):
    class Meta:
        model = EventSettings
        exclude = ["id"]
        read_only = True
