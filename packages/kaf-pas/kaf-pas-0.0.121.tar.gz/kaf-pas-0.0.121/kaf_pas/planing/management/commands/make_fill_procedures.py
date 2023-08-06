import logging

from django.core.management import BaseCommand
from django.db import transaction

from isc_common.common.mat_views import create_insert_update_delete_function_of_table

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        exclude_fields = [
            'arranges_exucutors',
            'exucutors',
            'id_f',
            'isFolder',
            'location_ids',
            'location_sectors_full_name',
            'location_sectors_ids',
            'parent_id',
            'props',
        ]

        with transaction.atomic():
            print(f'creating insert_update_delete_function_of_table: planing_production_order_tbl')
            create_insert_update_delete_function_of_table(table_name='planing_production_order', exclude_fields=exclude_fields)
            print(f'created insert_update_delete_function_of_table: planing_production_order_tbl')

            print(f'creating insert_update_delete_function_of_table: planing_production_order_per_launch_tbl')
            create_insert_update_delete_function_of_table(
                table_name='planing_production_order_per_launch',
                func_params=[('id', 'bigint'), ('launch_id', 'bigint')],
                exclude_fields=exclude_fields
            )
            print(f'created insert_update_delete_function_of_table: planing_production_order_per_launch_tbl')
