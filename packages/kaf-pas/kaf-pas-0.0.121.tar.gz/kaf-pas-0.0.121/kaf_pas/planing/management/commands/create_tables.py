import logging

from django.core.management import BaseCommand

from isc_common.auth.models.user import User

logger = logging.getLogger(__name__)


def create_production_order_tmp_tables():
    from isc_common.common.mat_views import create_table, create_insert_update_delete_function_of_table, refresh_mat_view

    refresh_mat_view('accounting_buffers_mview')

    tablenames = ['planing_production_order']

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

    for tablename in tablenames:
        table_name_tbl = f'''{tablename}_tbl'''
        print(f'Creating: {table_name_tbl}')

        create_table(
            sql_str=f'''select * from {tablename}_view''',
            table_name=table_name_tbl,
            primary_key=[
                'id',
                'parent_id',
                'id_f',
            ],
            indexes=[
                'date',
                'id',
                'isDeleted',
                'item_id',
                'launch_id',
                'num',
                'opertype_id',
                'parent_id',
                'parent_item_id',
                'props',
                'id_f',
                'status_id',
            ],
            unique_indexes=[
                'id',
                'id_f',
                'parent_id',
            ],
            any_constraints=[f'''ALTER TABLE {table_name_tbl}
                                         ADD CONSTRAINT {table_name_tbl}_pk_ciurate
                                             check(NOT(id=parent_id));''']
        )
        print(f'Created: {table_name_tbl}')
        print(f'Creating insert_update_delete_function_of_table: {table_name_tbl}')

        create_insert_update_delete_function_of_table(table_name=tablename, exclude_fields=exclude_fields)
        print(f'Created insert_update_delete_function_of_table: {table_name_tbl}')

    tablenames = ['planing_production_order_per_launch']

    for tablename in tablenames:
        table_name_tbl = f'''{tablename}_tbl'''
        print(f'Creating: {table_name_tbl}')

        create_table(
            sql_str=f'''select * from {tablename}_view''',
            table_name=table_name_tbl,
            primary_key=[
                'id',
                'id_f',
                'launch_id',
                'parent_id',
            ],
            indexes=[
                'date',
                'id',
                'item_id',
                'launch_id',
                'num',
                'opertype_id',
                'parent_id',
                'parent_item_id',
                'props',
                'id_f',
                'status_id',
            ],
            unique_indexes=[
                'id',
                'id_f',
                'launch_id',
                'parent_id',
            ],
            any_constraints=[f'''ALTER TABLE {table_name_tbl}
                             ADD CONSTRAINT {table_name_tbl}_pk_ciurate
                                 check(NOT(id=parent_id));''']
        )

        print(f'Created: {table_name_tbl}')
        print(f'Creating insert_update_delete_function_of_table: {table_name_tbl}')

        create_insert_update_delete_function_of_table(
            table_name=tablename,
            func_params=[('id', 'bigint'), ('launch_id', 'bigint')],
            exclude_fields=exclude_fields
        )

        print(f'Created insert_update_delete_function_of_table: {table_name_tbl}')


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--user_id', type=int)

    def handle(self, *args, **options):
        from isc_common.common import doing
        from kaf_pas.planing.models.production_ext import Production_ext
        from kaf_pas.planing.models.production_order import Production_order
        from kaf_pas.planing.models.production_order_per_launch import Production_order_per_launch
        from kaf_pas.production.models.launches import Launches

        user_id = options.get('user_id')
        if user_id is None:
            raise Exception('Not used --user_id')

        create_production_order_tmp_tables()

        ids = list(map(lambda x: x.id, Production_order.objects.exclude(status__code=doing)))
        print(f'check_state: Production_order')
        Production_order.objects.filter(id__in=ids).check_state()

        print(f'check_state: Production_order_per_launch')
        ids = list(map(lambda x: x.id, Production_order_per_launch.objects.exclude(status__code=doing)))
        Production_order_per_launch.objects.filter(id__in=ids).check_state()

        production_ext = Production_ext()
        print('grouping1')
        launch_ids=list(map(lambda x: x.id, Launches.objects.filter(parent=None).exclude(code='Нет')))
        print(f'launch_ids: {launch_ids}')
        production_ext.grouping1(launch_ids=launch_ids)
        print('fill_locations_sector_ready')
        production_ext.fill_locations_sector_ready(launch_ids=list(map(lambda x: x.id, Launches.objects.all())), user=User.objects.get(id = user_id))
        print('Done.')
