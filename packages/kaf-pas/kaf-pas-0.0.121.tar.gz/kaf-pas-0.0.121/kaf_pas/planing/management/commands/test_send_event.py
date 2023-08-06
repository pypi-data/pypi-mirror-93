import logging

from django.conf import settings
from django.core.management import BaseCommand
from django.db import transaction

from isc_common.auth.models.user import User
from isc_common.common import blinkString
from isc_common.common.functions import ExecuteStoredProc
from isc_common.ws.webSocket import WebSocket

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        settings.EVENT_STACK.EVENTS_PRODUCTION_ORDER_CREATE.send_message(
            message=blinkString(f'<h4>Удалиено: 100 заданий на производство.</h4>', bold=True),
            users_array=[User.objects.get(id=44)],
        )

