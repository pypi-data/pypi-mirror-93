import logging

from django.db import transaction

from isc_common import Stack
from isc_common.common.base_command import BaseCommand
from kaf_pas.planing.models.production_order import Production_order

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        with transaction.atomic():
            from kaf_pas.planing.models.production_order_values_ext import Production_order_values_ext
            production_order_values_ext = Production_order_values_ext()

            production_record = Production_order.objects.get(id=454094)
            comments = Stack()

            _qty = production_order_values_ext.subtraction_from_inventory(
                production_record=production_record,
                user=self.user,
                comments=comments,
                _qty=20
            )

            raise Exception('Not')
