import logging

from django.core.management import BaseCommand
from django.db import transaction

from isc_common.common.functions import ExecuteStoredProc

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        with transaction.atomic():
            # res = ExecuteStoredProc('get_production_order_ready', [465595, 27, [12], 'planing_production_order_tbl'])
            res = ExecuteStoredProc('get_production_order_operation_ready', [468484, 27, 468490])
            print(f'res={res}')
