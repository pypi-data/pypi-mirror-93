import logging

from django.core.management import BaseCommand

from isc_common.auth.models.user import User
from kaf_pas.planing.models.production_order import Production_orderManager, Production_order

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        Production_orderManager.update_location_sectors_full_name(
            ids=[458787, 458752],
            model=Production_order,
            user=User.objects.get(id=2)
        )
