import itertools
import logging

from django.core.management import BaseCommand
from django.db import transaction
from tqdm import tqdm

from kaf_pas.planing.models.production_order import Production_orderManager, Production_order

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        with transaction.atomic():
            Production_orderManager.update_redundant_planing_production_order_table([428646])
