from django.core.management.base import BaseCommand, CommandError
from acc_server.services import ServerWorkerManager


class Command(BaseCommand):

    def handle(self, *args, **options):
        # try:
        manager = ServerWorkerManager()
        manager.polling()
        # except Exception as e:
        #     print(e)
