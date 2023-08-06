import logging

from django.core.management import BaseCommand
from django.db import connection, transaction

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--launch_id', type=int)

    def handle(self, *args, **options):
        from kaf_pas.production.models.launches import Launches
        from isc_common.common.functions import ExecuteStoredProc
        from isc_common.common.mat_views import create_insert_update_delete_function_of_table, refresh_mat_view
        from kaf_pas.planing.models.production_ext import Production_ext

        launch_id = options.get('launch_id')


        production_ext = Production_ext()
        production_ext.create_s_table()

        with transaction.atomic():
            refresh_mat_view('accounting_buffers_mview')

            sql_str = '''select distinct porf.parent_id
                                    from planing_operation_refs porf
                                        join planing_operation_launches polch ON polch.operation_id = porf.child_id
                                    where polch.launch_id=%s'''

            launch = Launches.objects.get(id=launch_id)
            if launch.parent is None:
                with connection.cursor() as cursor:
                    cursor.execute(sql_str, [launch.id])
                    rows = cursor.fetchall()

                ids = list(map(lambda x: x[0], rows))

                print(f'moving data table: planing_production_order_tbl qty: {len(ids)}')
                ExecuteStoredProc('update_planing_production_order_s', [ids])
                print(f'moved data table: planing_production_order_tbl')
            else:
                with connection.cursor() as cursor:
                    cursor.execute(sql_str, [launch.id])
                    rows = cursor.fetchall()

                ids = list(map(lambda x: x[0], rows))

                print(f'moving data table: planing_production_order_per_launch_tbl qty: {len(ids)}')
                ExecuteStoredProc('update_planing_production_order_per_launch_s', [ids])
                print(f'moved data table: planing_production_order_per_launch_tbl')
