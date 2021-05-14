from django.test import TestCase
from acc_server.services.server_worker import ServerWorker
from acc_server.models import AccEvent
from django.contrib.auth.models import User
from django.utils import timezone
from acc_server.services import ServerWorkerManager


class ServerWorkerInitCwdTest(TestCase):

    def setUp(self) -> None:
        user = User.objects.create_user(username='burenotti', email="burenotti@gmail.com", password="123456")
        event = AccEvent()
        event.save()

    def test(self) -> None:
        creator = User.objects.get(username='burenotti')
        event = AccEvent.objects.all()[0]
        manager = ServerWorkerManager()
        worker = manager.create_worker(event)
        worker.init_cwd()
        worker.run()