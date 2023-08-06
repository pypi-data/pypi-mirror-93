import logging

from django.core.management import BaseCommand
from django.db import transaction

from isc_common import StackWithId
from kaf_pas.planing.models.production_ext import Production_ext, User_ready_struct

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        from kaf_pas.planing.models.production_order import Production_order
        from kaf_pas.planing.models.production_order_per_launch import Production_order_per_launch

        production_ext = Production_ext()

        # user_ready_struct, user, model, key = None
        model = None

        user_ready_struct = User_ready_struct(
            id=479827,
            table_name_tbl='planing_production_order_tbl',
            location_ids=[12],
            stack=StackWithId()
        )
        if user_ready_struct.table_name_tbl == 'planing_production_order_tbl':
            model = Production_order
        elif user_ready_struct.table_name_tbl == 'planing_production_order_per_launch_tbl':
            model = Production_order_per_launch

        with transaction.atomic():
            production_ext.set_ready_up(user=2, model=model, user_ready_struct=user_ready_struct, location_sector_ids=[])
