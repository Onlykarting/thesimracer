from django.http import JsonResponse
from acc_server.serializers import ServerConfigSerializer, ServerSettingsSerializer, AssistRulesSerializer, \
    EventSettingsSerializer, EventRulesSerializer


class BaseConfigDumper:

    def __init__(self, context, query_set, serializer, file_path: str = None):
        self.context = context
        self.file_path = file_path
        self.serializer = serializer
        self.query_set = query_set

    def dump(self):
        with open(self.file_path, 'w') as file:
            file.write(JsonResponse(self.serializer(self.query_set).data).content.decode('utf-8'))
            # file.write(str(self.serializer(self.query_set).data))


class ServerConfigDumper(BaseConfigDumper):

    def __init__(self, context):
        super().__init__(context,
                         context.event.server_config,
                         ServerConfigSerializer,
                         context.config_path / 'configuration.json')


class ServerSettingsDumper(BaseConfigDumper):
    def __init__(self, context):
        super().__init__(context,
                         context.event.server_settings,
                         ServerSettingsSerializer,
                         context.config_path / 'settings.json')


class AssistRulesDumper(BaseConfigDumper):
    def __init__(self, context):
        super().__init__(context,
                         context.event.assist_rules,
                         AssistRulesSerializer,
                         context.config_path / 'assistRules.json')


class EventSettingsDumper(BaseConfigDumper):
    def __init__(self, context):
        super().__init__(context,
                         context.event.event_settings,
                         EventSettingsSerializer,
                         context.config_path / 'event.json')


class EventRulesDumper(BaseConfigDumper):
    def __init__(self, context):
        super().__init__(context,
                         context.event.event_rules,
                         EventRulesSerializer,
                         context.config_path / 'eventRules.json')