import logging

from django.core.management import BaseCommand
from django.db import transaction

from kaf_pas.planing.models.production_ext import Production_ext

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--launch_id', type=int)

    def handle(self, *args, **options):
        launch_id = options.get('launch_id')

        production_ext = Production_ext()
        production_ext.grouping1(launch_ids=[launch_id])
