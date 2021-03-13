from django.test import TestCase
from acc_server.services.server_worker import ServerWorker
from acc_server.models import ServerWorkerSettings, Event, Playlist
from django.contrib.auth.models import User
from django.utils import timezone
from acc_server.services import ServerWorkerManager


class ServerWorkerInitCwdTest(TestCase):

    def setUp(self) -> None:
        user = User.objects.create_user(username='burenotti', email="burenotti@gmail.com", password="123456")
        playlist = Playlist.objects.create(name="Тестовый чемпионат", creator=user)
        event = Event.objects.create(name="Раунд 1", playlist=playlist, starts_at=timezone.now())  # <-- ломается здесь
        ServerWorkerSettings.objects.create(event=event, status=ServerWorkerSettings.PLANNED)

    def test(self) -> None:
        creator = User.objects.get(username='burenotti')
        settings = ServerWorkerSettings.objects.get(event__playlist__creator=creator)
        manager = ServerWorkerManager()
        worker = manager.create_worker(settings)
        worker.init_cwd()
        worker.run()
