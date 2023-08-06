import logging

from django.core.management import BaseCommand

from isc_common.auth.models.user import User
from kaf_pas.planing.models.production_ext import Production_ext

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    production_ext = Production_ext()

    def handle(self, *args, **options):
        from kaf_pas.production.models.launches import Launches
        self.production_ext.fill_locations_sector_ready(launch_ids=list(map(lambda x: x.id, Launches.objects.all())), user=User.objects.get(id=2))
