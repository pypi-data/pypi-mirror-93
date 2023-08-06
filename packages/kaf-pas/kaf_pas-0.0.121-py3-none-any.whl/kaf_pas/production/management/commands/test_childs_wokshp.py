import logging

from django.core.management import BaseCommand

from kaf_pas.ckk.models.locations import Locations

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Тестирование"

    def handle(self, *args, **options):
        for location in Locations.objects_tree.get_descendants(id=12, child_id='id', include_self=False):
            print(location)
