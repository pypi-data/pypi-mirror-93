import logging
from decimal import Decimal

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import EmptyResultSet
from django.db import transaction, connection
from django.db.models import DecimalField, DateTimeField, TextField, BooleanField, BigIntegerField, PositiveIntegerField, SmallIntegerField
from django.forms import model_to_dict

from isc_common import setAttr, Wrapper, dictinct_list
from isc_common.auth.models.user import User
from isc_common.common import blinkString, started, new, doing, sht, blinkString1, green, to_H, blue
from isc_common.common.functions import ExecuteStoredProc
from isc_common.datetime import DateTimeToStr
from isc_common.fields.code_field import CodeField, JSONFieldIVC
from isc_common.fields.related import ForeignKeyProtect, ForeignKeyCascade
from isc_common.http.DSRequest import DSRequest
from isc_common.json import StrToJson
from isc_common.managers.common_manager import CommonManager
from isc_common.models.audit import AuditQuerySet, AuditModel
from isc_common.models.tree_audit import TreeAuditModelManager
from isc_common.number import DecimalToStr, ToDecimal, model_2_dict
from isc_common.ws.webSocket import WebSocket
from kaf_pas.ckk.models.ed_izm import Ed_izm
from kaf_pas.ckk.models.item import Item
from kaf_pas.planing.models.operation_types import Operation_types
from kaf_pas.planing.models.operations import Operations
from kaf_pas.planing.models.production_ext import Production_ext, Operation_executor_stack, RecordAttrs
from kaf_pas.planing.models.production_order_values_ext import Production_order_values_ext
from kaf_pas.planing.models.rouning_ext import Routing_ext
from kaf_pas.planing.operation_typesStack import DETAIL_OPERS_PRD_TSK
from kaf_pas.production.models.launches import Launches

logger = logging.getLogger(__name__)


class Production_orderQuerySet(AuditQuerySet):
    production_ext = Production_ext()
    production_order_values_ext = Production_order_values_ext()
    edizm_shtuka = Ed_izm.objects.get(code=sht)

    status_new = settings.OPERS_TYPES_STACK.PRODUCTION_TASK_STATUSES.get(new)
    status_doing = settings.OPERS_TYPES_STACK.PRODUCTION_TASK_STATUSES.get(doing)
    status_started = settings.OPERS_TYPES_STACK.PRODUCTION_TASK_STATUSES.get(started)

    @classmethod
    def get_user_locations(cls, user):
        from kaf_pas.ckk.models.locations_users import Locations_users
        if not user.is_admin and not user.is_develop:
            return list(set(map(lambda x: x.location.id, Locations_users.objects.filter(user=user).distinct())))
        else:
            return None

    def check_state(self):
        for this in self:
            if ToDecimal(this.value_odd) > 0 and ToDecimal(this.value_start) > 0:
                status = self.status_started
            elif ToDecimal(this.value_start) == 0:
                status = self.status_new
            else:
                if ToDecimal(this.value_start) >= ToDecimal(this.value_sum):
                    status = self.status_doing
                else:
                    status = self.status_started

            updated = super().filter(id=this.id).update(status=status)
            logger.debug(f'updated: {updated}')
            updated = Operations.objects.filter(id=this.id).update(status=status)
            logger.debug(f'updated: {updated}')

    def get_range_rows(self, start=None, end=None, function=None, json=None, distinct_field_names=None, user=None, *args, **kwargs):
        from kaf_pas.production.models.operation_executor import Operation_executor
        from kaf_pas.production.models.operation_def_resources import Operation_def_resources

        queryResult = self._get_range_rows(*args, start=start, end=end, function=function, json=json, distinct_field_names=distinct_field_names)

        try:
            logger.debug(f'\n\n{queryResult.query}\n')
        except EmptyResultSet:
            pass

        if function:
            location_ids = Production_orderQuerySet.get_user_locations(user=user)
            executor_operation_ids = Operation_executor.executor_operation_ids(user=user)

            executor_operation_location_ids = []
            if len(executor_operation_ids) > 0:
                executor_operation_location_ids.extend(list(set(map(lambda x: x.location.id, Operation_def_resources.objects.filter(operation_id__in=executor_operation_ids)))))

            res = [function(
                record,
                location_ids,
                user,
                self.model,
                executor_operation_ids,
                executor_operation_location_ids,
            ) for record in queryResult]
            return res
        else:
            res = [model_to_dict(record) for record in queryResult]
            return res

    def get_range_rows1(self, request, function=None, distinct_field_names=None, remove_fields=None, *args, **kwargs):
        request = DSRequest(request=request)
        data = request.get_data()

        _data = data.copy()
        if _data.get('criteria') is not None:

            criteria = list(filter(lambda x: x.get('fieldName') not in ['location_id', 'arranged'], _data.get('criteria')))
            criteria1 = list(filter(lambda x: x.get('fieldName') == 'parent_id' and x.get('value') == None and x.get('operator') == 'notEqual', criteria))

            if len(criteria1) > 0:
                criteria = list(filter(lambda x: x.get('fieldName') != 'parent_id', criteria))
            #     criteria.append(dict(fieldName='parent_id', value=None, operator='equals'))

            setAttr(_data, 'criteria', criteria)

        request.set_data(_data)

        self.alive_only = request.alive_only
        self.enabledAll = request.enabledAll
        res = self.get_range_rows(
            start=request.startRow,
            end=request.endRow,
            function=function,
            distinct_field_names=distinct_field_names,
            json=request.json,
            criteria=request.get_criteria(),
            user=request.user,
        )
        return res

    def get_setStartStatus(self, request):

        request = DSRequest(request=request)

        data = request.get_data()
        return self.production_ext.get_setStartStatus(data=data, user=request.user)

    def get_setMadedStatus(self, request):
        from kaf_pas.planing.models.production_order_tmp_ext import Production_order_tmp_ext

        request = DSRequest(request=request)

        data = request.get_data()
        value = data.get('qty')

        _res = []

        if request.user.is_admin:
            raise Exception('Операция внесения данных по запуску не работает из режима Администратора.')

        res = self.production_ext.get_FinishFormType(data=data, user=request.user, with_out_view=True)
        setAttr(data, 'value', value)
        setAttr(data, 'process', res.get('process'))
        setAttr(data, 'order_model', res.get('order_model'))

        production_order_tmp_ext = Production_order_tmp_ext()
        res = production_order_tmp_ext.set_Count(data=data, user=request.user)

        _res = self.production_ext.get_setFinishStatus(data=data, user=request.user)

        return _res

    def get_setFinishStatus(self, request):

        request = DSRequest(request=request)

        data = request.get_data()
        return self.production_ext.get_setFinishStatus(data=data, user=request.user)

    def get_FinishFormType(self, request):

        request = DSRequest(request=request)
        data = request.get_data()

        return self.production_ext.get_FinishFormType(data=data, user=request.user)

    def getLoocationUsers(self, request):
        from kaf_pas.ckk.models.locations_users import Locations_users
        from isc_common.auth.managers.user_manager import UserManager

        request = DSRequest(request=request)
        data = request.get_data()

        location_sector_ids = set()
        for record in data.get('location_sector_ids'):
            for location_sector_id in record:
                location_sector_ids.add(location_sector_id)
                break

        if len(location_sector_ids) != 1:
            location_sector_ids = []
        else:
            location_sector_ids = list(location_sector_ids)

        location_id = data.get('location_id')

        parent_query = Locations_users.objects.filter(location_id__in=location_sector_ids, user=request.user)
        parent = None
        if parent_query.count() > 0:
            parent = parent_query[0]

        if parent is None:
            parent_query = Locations_users.objects.filter(location_id=location_id, user=request.user)
            if parent_query.count() > 0:
                parent = parent_query[0]

        res = [UserManager.getRecord1(item.user).get('id') for item in Locations_users.objects.filter(location_id=location_id, parent=parent)]
        res1 = [UserManager.getRecord1(item.user).get('id') for item in Locations_users.objects.filter(location_id__in=location_sector_ids)]

        res2 = list(set(res).intersection(res1))
        return [UserManager.getRecord1(User.objects.get(id=id)) for id in res2]


class TemplateItem:
    parent_id = None
    child_id = None

    def __init__(self, parent_id, child_id):
        self.parent_id = parent_id
        self.child_id = child_id


class WrapperRefresh_all(Wrapper):
    ids = None
    buffer_refresh = False
    item_operations_refresh = False
    production_order_values_refresh = False
    production_order_opers_refresh = False
    production_order_rows_refresh = True
    production_order_opers_ids = None
    user = None
    suffix = None
    model = None


class Production_orderManager(CommonManager):
    production_ext = Production_ext()
    routing_ext = Routing_ext()

    @classmethod
    def ids_list_2_opers_list(cls, ids):
        from isc_common.models.audit import AuditModel

        if ids is None:
            return []

        ls_res = []

        if not isinstance(ids, list):
            ids = [ids]

        for id in ids:
            if isinstance(id, int):
                try:
                    ls_res.append(Operations.objects.get(id=id))
                except Operations.DoesNotExist:
                    pass
            elif isinstance(id, AuditModel):
                ls_res.append(id)
            else:
                raise Exception(f'{id} must be int or Operation')
        return ls_res

    @classmethod
    def ids_list_2_int_list(cls, ids):
        from isc_common.models.audit import AuditModel

        if ids is None:
            return []

        if isinstance(ids, map):
            ids = list(ids)

        if not isinstance(ids, list):
            ids = [ids]

        ls_res = []
        for id in ids:
            if isinstance(id, int):
                ls_res.append(id)
            elif isinstance(id, AuditModel):
                ls_res.append(id.id)
            else:
                raise Exception(f'{id} must be int or Operation')

        return ls_res

    @classmethod
    def refresh_all(
            cls,
            ids,
            buffer_refresh=False,
            item_operations_refresh=False,
            production_order_values_refresh=False,
            production_order_opers_refresh=False,
            production_order_rows_refresh=True,
            production_order_opers_ids=None,
            user=None,
            suffix=None,
            model=None
    ):
        from kaf_pas.planing.models.production_order_values import Production_order_valuesManager
        from kaf_pas.accounting.models.buffers import BuffersManager
        from kaf_pas.ckk.models.item_operations_view import Item_operations_viewManager
        from kaf_pas.planing.models.production_order_opers import Production_order_opersManager

        if ids is None:
            return

        if isinstance(ids, map):
            ids = list(ids)

        Production_orderManager.update_redundant_planing_production_order_table(ids=ids, user=user, model=model)
        Production_order.objects.filter(id__in=Production_orderManager.ids_list_2_int_list(ids)).check_state()

        # if production_order_rows_refresh is True:
        #     Production_orderManager.refreshRows(ids=ids, user=user, model=model)
        # else:
        #     Production_orderManager.fullRows(suffix=suffix)

        if buffer_refresh is True:
            BuffersManager.fullRows()

        if item_operations_refresh is True:
            Item_operations_viewManager.fullRows()

        if production_order_values_refresh is True:
            Production_order_valuesManager.fullRows()

        if production_order_opers_refresh is True:
            if production_order_opers_ids is not None:
                Production_order_opersManager.refreshRows(ids=production_order_opers_ids, user=user)
            else:
                Production_order_opersManager.fullRows()

    @classmethod
    def update_redundant_planing_production_order_table(
            cls,
            ids,
            user,
            model=None
    ):
        from kaf_pas.planing.models.production_order_per_launch import Production_order_per_launch
        from django.db.models import Model

        production_ext = Production_ext()

        if isinstance(ids, list):
            if model is None:
                model = Production_order
                for production_order in model.objects.filter(id__in=ids):
                    production_ext.updateModelRow(
                        id=production_order.id,
                        id_f=production_order.id_f,
                        launch_id=production_order.launch_id,
                        location_ids=production_order.location_ids,
                        model=model,
                        status=production_order.status,
                        update_ready_struct=True,
                        user=user,
                    )
                Production_orderManager.refreshRows(ids=ids, model=model, user=user)

                model = Production_order_per_launch
                for production_order in model.objects.filter(id__in=ids):
                    production_ext.updateModelRow(
                        id=production_order.id,
                        id_f=production_order.id_f,
                        launch_id=production_order.launch_id,
                        location_ids=production_order.location_ids,
                        model=model,
                        status=production_order.status,
                        update_ready_struct=True,
                        user=user,
                    )
                Production_orderManager.refreshRows(ids=ids, model=model, user=user)
            else:
                production_orders = model.objects.filter(id__in=ids)
                for production_order in production_orders:
                    production_ext.updateModelRow(
                        id=production_order.id,
                        id_f=production_order.id_f,
                        launch_id=production_order.launch_id,
                        location_ids=production_order.location_ids,
                        model=model,
                        status=production_order.status,
                        update_ready_struct=True,
                        user=user,
                    )
                Production_orderManager.refreshRows(ids=ids, model=model, user=user)


        elif isinstance(ids, Model):
            cls.update_redundant_planing_production_order_table([ids.id], user=user, model=model)
        elif isinstance(ids, int):
            cls.update_redundant_planing_production_order_table([ids], user=user, model=model)
        else:
            raise Exception('Ошибочный тип параметра')

    @classmethod
    def delete_redundant_planing_production_order_table(cls, id):

        if id is None:
            raise Exception('id must be not None')

        settings.LOCKS.acquire(settings.GRID_CONSTANTS.lock_insert_update_delete_function_of_table)

        try:
            ids = Production_orderManager.ids_list_2_int_list(id)

            for id in ids:
                with connection.cursor() as cursor:
                    cursor.execute('''select id
                                      from production_launches
                                      where parent_id in (select launch_id
                                                          from planing_operation_launches
                                                          where operation_id = %s)''', [id])
                    rows = cursor.fetchall()
                    for row in rows:
                        launch_id, = row
                        res = ExecuteStoredProc('delete_planing_production_order_per_launch', [id, launch_id])
                        logger.debug(f'id: {res}')

                ExecuteStoredProc('delete_planing_production_order', [id])

            settings.LOCKS.release(settings.GRID_CONSTANTS.lock_insert_update_delete_function_of_table)
        except Exception as ex:
            settings.LOCKS.release(settings.GRID_CONSTANTS.lock_insert_update_delete_function_of_table)
            logger.error(ex)

    @classmethod
    def update_location_sectors_full_name(cls, ids, model, user):

        ids = Production_orderManager.ids_list_2_int_list(ids)
        location_ids = Production_orderQuerySet.get_user_locations(user=user)

        for id in ids:

            for production_order in model.objects.filter(id=id):
                location_sectors_full_name = ExecuteStoredProc('get_location_sectors_full_name', [id, location_ids])

                if production_order.location_sector_ids is not None:
                    model.objects.filter(
                        id=production_order.id,
                        id_f=production_order.id_f,
                        parent_id=production_order.parent_id,
                        launch=production_order.launch).update(location_sectors_full_name=location_sectors_full_name)

        Production_orderManager.refreshRows(ids=ids, user=user, model=model)

    @classmethod
    def update_executors(cls, ids, model, user):

        ids = Production_orderManager.ids_list_2_int_list(ids)
        for id in ids:

            for production_order in model.objects.filter(id=id):
                with connection.cursor() as cursor:
                    cursor.execute('''select array_agg(distinct executor_id)
                                        from planing_operation_executor po
                                        where po.operation_id = %s
                                          and is_bit_on(props, 0) = true
                                          and is_bit_on(props, 1) = false''', [id])

                    row = cursor.fetchone()
                    exucutors, = row

                    model.objects.filter(
                        id=production_order.id,
                        id_f=production_order.id_f,
                        parent_id=production_order.parent_id,
                        launch=production_order.launch).update(exucutors=exucutors)

        Production_orderManager.refreshRows(ids=ids, user=user)

    def forwardingGroupingTree(self, parent_id, model, executors=None, arranges_exucutors=None, id=None, id_f=None):
        if id is not None and id_f is not None:
            query = model.objects.filter(id=id, id_f=id_f, parent_id=parent_id)
        else:
            query = model.objects.filter(id_f=parent_id)

        for oper in query:
            logger.debug(f'\noper: {oper}')
            logger.debug(f'\nexecutors: {executors}')
            logger.debug(f'\narranges_exucutors: {arranges_exucutors}')

            _arranges_exucutors = set()
            if arranges_exucutors is not None:
                if isinstance(arranges_exucutors, int):
                    arranges_exucutors = [arranges_exucutors]

                _arranges_exucutors = _arranges_exucutors.union(set(arranges_exucutors))
                updated = model.objects.filter(id=oper.id, id_f=oper.id_f, parent_id=oper.parent_id).update(arranges_exucutors=list(_arranges_exucutors))

            if executors is not None:
                if oper.isFolder is False:
                    _exucutors = set(oper.exucutors).difference(_arranges_exucutors)
                else:
                    _exucutors = set(oper.exucutors)
                _exucutors = _exucutors.union(set(executors))
                _exucutors = list(_exucutors)
                updated = model.objects.filter(id=oper.id, id_f=oper.id_f, parent_id=oper.parent_id).update(exucutors=_exucutors)

            parent_id = oper.parent_id
            if parent_id is not None:
                self.forwardingGroupingTree(parent_id=parent_id, model=model, executors=_exucutors, arranges_exucutors=list(_arranges_exucutors))

    def updateFromRequestUpdateForwarding(self, request):
        from kaf_pas.planing.models.production_order_per_launch import Production_order_per_launch

        request = DSRequest(request=request)

        data = request.get_data()
        executors = data.get('executors')

        idx = 0
        with transaction.atomic():
            operation_executor_stack = Operation_executor_stack()
            while True:
                _data = data.get(str(idx))
                if _data is None:
                    break
                idx += 1

                operation_id = _data.get('id')
                operation_id_f = _data.get('id_f')
                parent_id = _data.get('parent_id')
                description = _data.get('description')

                Operations.objects.update_or_create(id=operation_id, defaults=dict(description=description))

                self.production_ext.set_executors(
                    executors=[User.objects.get(id=id) for id in executors],
                    operation=Operations.objects.get(id=operation_id),
                    user=request.user,
                    operation_executor_stack=operation_executor_stack
                )

                self.forwardingGroupingTree(id=operation_id, id_f=operation_id_f, parent_id=parent_id, executors=executors, arranges_exucutors=request.user.id, model=Production_order)
                self.forwardingGroupingTree(id=operation_id, id_f=operation_id_f, parent_id=parent_id, executors=executors, arranges_exucutors=request.user.id, model=Production_order_per_launch)

                Production_order.objects.filter(id=operation_id).check_state()
                Production_order_per_launch.objects.filter(id=operation_id).check_state()

            for operation_executor in operation_executor_stack:
                settings.EVENT_STACK.EVENTS_PRODUCTION_ORDER_CREATE.send_message(
                    message=blinkString(to_H(f'Вам направлено: {operation_executor.qty} новых заданий на производство.'), bold=True, blink=False, color=blue),
                    users_array=[operation_executor.executor],
                )
                Production_orderManager.fullRows(suffix=f'''_user_id_{operation_executor.executor.id}''')

        return data

    def createFromRequest(self, request):

        request = DSRequest(request=request)
        data = request.get_data()

        production_ext = Production_ext()
        production_ext.make_production_order_by_hand(data=data, user=request.user)

        return data

    def get_queryset(self):
        return Production_orderQuerySet(self.model, using=self._db)

    @classmethod
    def refreshRows(cls, ids, user, model=None, location_ids=None, executor_operations_ids=None):
        from kaf_pas.production.models.operation_executor import Operation_executor
        from kaf_pas.production.models.operation_def_resources import Operation_def_resources

        if model is None:
            model = Production_order

        if user is None or (isinstance(ids, list) and len(ids) == 0):
            return

        ids = Production_orderManager.ids_list_2_int_list(ids)
        res_ids = []

        for id in ids:
            res_ids = list(set(res_ids).union(set(map(lambda x: x.id, model.tree_objects.get_parents(id=id, child_id='id_f', include_self=False)))))

        if location_ids is None:
            location_ids = Production_orderQuerySet.get_user_locations(user=user)

        if executor_operations_ids is None:
            executor_operations_ids = Operation_executor.executor_operation_ids(user=user)

        if isinstance(location_ids, list):
            location_ids=list(set(location_ids))
        executor_operation_location_ids = location_ids

        if len(executor_operations_ids) > 0:
            executor_operation_location_ids.extend(list(set(map(lambda x: x.location.id, Operation_def_resources.objects.filter(operation_id__in=executor_operations_ids)))))

        records = [Production_orderManager.getRecord(
            record=record,
            location_ids=location_ids,
            executor_operations_ids=executor_operations_ids,
            executor_operation_location_ids=executor_operation_location_ids,
            user=user,
            model=model
        ) for record in model.objects.filter(id__in=res_ids)]

        suffix = f'_user_id_{user.id}'

        WebSocket.row_refresh_grid(grid_id=f'{settings.GRID_CONSTANTS.refresh_production_order_grid_row}{suffix}', records=records)

    @classmethod
    def fullRows(cls, suffix=''):
        WebSocket.full_refresh_grid(grid_id=f'{settings.GRID_CONSTANTS.refresh_production_order_grid}{suffix}')

    @classmethod
    def get_executor_operations_ids(cls, executor_operations_ids, record):
        # executor_operations_ids_set = set(executor_operations_ids)
        # s_set = set(record.location_sector_ids) if record.location_sector_ids is not None else set()
        # executor_operations_ids = list(executor_operations_ids_set.intersection(s_set))

        # if record.isFolder is False:
        #     return []
        return executor_operations_ids

    @classmethod
    def getRecord_attrs(cls, record, location_ids, executor_operations_ids, executor_operation_location_ids, user, model, tmp=False):
        from isc_common.number import Set

        record_id = record.id_real if hasattr(record, 'id_real') else record.id
        value_start = ToDecimal(record.value_start)
        item__STMP_1__value_str = record.item.STMP_1.value_str if record.item.STMP_1 else None
        launch__code = record.launch.code
        location_sectors_ready = None

        if value_start != 0:
            percents = round(ToDecimal(record.value_made) * 100 / ToDecimal(value_start), 2)
        else:
            percents = 0

        percents_str = "%.2f" % percents
        value_made = record.value_made

        if isinstance(location_ids, list):
            ls_set = set(location_ids)

            if item__STMP_1__value_str is not None:
                if isinstance(record.location_sectors_ready, dict) and isinstance(executor_operation_location_ids, list) and isinstance(location_ids, list):
                    executor_operation_location_ids.extend(location_ids)
                    locations_sector_ready_arr = list(filter(lambda x: x is not None and x != 0, map(lambda location_id: record.location_sectors_ready.get(str(location_id)), executor_operation_location_ids)))

                    if len(locations_sector_ready_arr) > 0:
                        location_sectors_ready = locations_sector_ready_arr[0]

                    if location_sectors_ready == 1:
                        item__STMP_1__value_str = to_H(f'{item__STMP_1__value_str} {blinkString1(text="&#128161;", color=green)}')

            s_set = set(record.location_sector_ids) if record.location_sector_ids is not None else set()
            location_ids = list(s_set.intersection(ls_set))
            location_ids = list(filter(lambda x: record.locations_sector_full_name.get(str(x)) != None, location_ids))

            if len(location_ids) > 0:
                status__name_arr = list(filter(lambda x: x is not None, map(lambda location_id: record.location_statuses.get(str(location_id)), location_ids)))

                status__color_arr = list(filter(lambda x: x is not None, map(lambda location_id: record.location_status_colors.get(str(location_id)), location_ids)))

                status__values_made_arr = list(filter(lambda x: x is not None, map(lambda location_id: record.location_values_made.get(str(location_id)), location_ids)))

                status_id_arr = list(filter(lambda x: x is not None, map(lambda location_id: record.location_status_ids.get(str(location_id)), location_ids)))

                locations_sector_full_name_arr = list(filter(lambda x: x is not None, map(lambda location_id: record.locations_sector_full_name.get(str(location_id)), location_ids)))

                if len(status__name_arr) > 0:
                    status__name = status__name_arr[0]
                else:
                    status__name = record.status.name

                if len(status__color_arr) > 0:
                    status__color = status__color_arr[0]
                else:
                    status__color = record.status.color

                if len(status_id_arr) > 0:
                    status_id = status_id_arr[0]
                else:
                    status_id = record.status.id

                if len(status__values_made_arr) > 0:
                    if tmp is False:
                        value_made = status__values_made_arr[0]

                    if value_start != 0:
                        percents = round(ToDecimal(value_made) * 100 / ToDecimal(value_start), 2)
                    else:
                        percents = 0

                    percents_str = "%.2f" % percents
                else:
                    location_values_made = ExecuteStoredProc('get_user_operations_values_made', [record_id, user.id])
                    if isinstance(location_values_made, str):
                        location_values_made = StrToJson(location_values_made)
                    if isinstance(location_values_made, dict):
                        status__values_made_arr = list(filter(lambda x: x is not None, map(lambda location_id: location_values_made.get(str(location_id)), location_ids)))

                        if len(status__values_made_arr) > 0:
                            if tmp is False:
                                value_made = status__values_made_arr[0]

                            if value_start != 0:
                                percents = round(ToDecimal(value_made) * 100 / ToDecimal(value_start), 2)
                            else:
                                percents = 0

                            percents_str = "%.2f" % percents

                if len(locations_sector_full_name_arr) > 0:
                    location_sectors_full_name = '<br>'.join(locations_sector_full_name_arr[0])
                else:
                    location_sectors_full_name = ''

                user_operations = None
                executor_operations_ids = cls.get_executor_operations_ids(executor_operations_ids=executor_operations_ids, record=record)
                if len(executor_operations_ids) > 0:
                    user_operations = ExecuteStoredProc('get_user_operations', [record_id, executor_operations_ids])

                if user_operations is not None:
                    location_sectors_full_name += f'<br>{user_operations}'
            else:
                status_id = record.status.id
                status__name = record.status.name
                status__color = record.status.color
                location_sectors_full_name = ''
                user_operations = None

                executor_operations_ids = cls.get_executor_operations_ids(executor_operations_ids=executor_operations_ids, record=record)
                if len(executor_operations_ids) > 0:
                    user_operations = ExecuteStoredProc('get_user_operations', [record_id, executor_operations_ids])

                if user_operations is not None:
                    location_sectors_full_name += f'<br>{user_operations}'
        else:
            status_id = record.status.id
            status__name = record.status.name
            status__color = record.status.color
            location_sectors_full_name = '<br>'.join(Set(record.location_sectors_full_name).get_set_sorted_as_original)

        if isinstance(record.value1_sum, Decimal):
            value1_sum = DecimalToStr(record.value1_sum)
            value1_sum_len = 0
        elif isinstance(record.value1_sum, list):
            value1_sum = ' / '.join([DecimalToStr(v) for v in record.value1_sum]) if record.value1_sum is not None else None
            value1_sum_len = len(record.value1_sum) if record.value1_sum is not None else None,
        else:
            value1_sum = ''
            value1_sum_len = 0

        return RecordAttrs(
            item__STMP_1__value_str=item__STMP_1__value_str,
            launch__code=launch__code,
            location_sectors_full_name=location_sectors_full_name,
            location_sectors_ready=location_sectors_ready,
            percents=percents,
            percents_str=percents_str,
            status__color=status__color,
            status__name=status__name,
            status_id=status_id,
            value1_sum=value1_sum,
            value1_sum_len=value1_sum_len,
            value_made=value_made,
        )

    @classmethod
    def getRecord(cls, record, location_ids, user, model, executor_operations_ids, executor_operation_location_ids):
        from isc_common.number import Set

        # if executor_operations_ids is None:
        #     executor_operations_ids = Operation_executor.executor_operation_ids(user=user)
        #
        # if executor_operation_location_ids is None:
        #     executor_operation_location_ids = Production_orderQuerySet.get_user_locations(user=user)

        record_attrs = cls.getRecord_attrs(
            executor_operation_location_ids=dictinct_list(executor_operation_location_ids),
            executor_operations_ids=dictinct_list(executor_operations_ids),
            location_ids=dictinct_list(location_ids),
            model=model,
            record=record,
            user=user,
        )

        item__STMP_1__value_str = record_attrs.item__STMP_1__value_str
        launch__code = record_attrs.launch__code
        location_sectors_full_name = record_attrs.location_sectors_full_name
        percents = record_attrs.percents
        percents_str = record_attrs.percents_str
        status__color = record_attrs.status__color
        status__name = record_attrs.status__name
        status_id = record_attrs.status_id
        value1_sum = record_attrs.value1_sum
        value1_sum_len = record_attrs.value1_sum_len
        value_made = record_attrs.value_made
        value_start = None if record.value_start == 0 else record.value_start

        if user.is_admin is True or user.is_develop is True:
            value_made_str = f'''{blinkString(DecimalToStr(value_made), blink=True if percents >= 100 else False, color="blue", bold=True)}({percents_str}%)'''
        else:
            value_made_str = f'''{blinkString(DecimalToStr(value_made), blink=True if percents >= 100 else False, color="blue", bold=True)}'''

        res = {
            'arranges_exucutors': sorted(record.arranges_exucutors) if record.arranges_exucutors is not None else None,
            'child_launches': record.child_launches,
            'cnt_opers': record.cnt_opers,
            'creator__short_name': record.creator.get_short_name,
            'date': record.date,
            'demand_ids': record.demand_ids,
            'demand_codes_str': record.demand_codes_str,
            'description': record.description,
            'edizm__name': ' / '.join(record.edizm_arr) if record.edizm_arr is not None else None,
            'exucutors': sorted(record.exucutors),
            'exucutors_old': sorted(record.exucutors_old),
            'id': record.id,
            'id_f': record.id_f,
            'isDeleted': record.isDeleted,
            'isFolder': record.isFolder if record.isFolder is not None else False,
            'item__STMP_1__value_str': item__STMP_1__value_str,
            'item__STMP_2__value_str': record.item.STMP_2.value_str if record.item.STMP_2 else None,
            'item_id': record.item.id,
            'launch__code': launch__code,
            'launch__date': record.launch.date,
            'launch_id': record.launch.id,
            'location_ids': record.location_ids,
            'location_ids_old': record.location_ids_old,
            'location_sector_ids': Set(record.location_sector_ids).get_set_sorted_as_original,
            'location_sectors_full_name': location_sectors_full_name,
            'max_level': record.max_level,
            'num': record.num,
            'opertype__full_name': record.opertype.full_name,
            'opertype_id': record.opertype.id,
            'parent_id': record.parent_id,
            'parent_item_id': record.parent_item.id if record.parent_item is not None else None,
            'parent_item_ids': record.parent_item_ids,
            'props': record.props,
            'status__code': record.status.code,
            'status__name': blinkString(text=status__name, blink=False, color=status__color, bold=True),
            'status_id': status_id,
            'value1_sum': value1_sum,
            'value1_sum_len': value1_sum_len,
            'value_made': DecimalToStr(value_made),
            'value_made_str': value_made_str,
            'value_odd': DecimalToStr(record.value_odd),
            'value_start': DecimalToStr(value_start),
            'value_sum': DecimalToStr(record.value_sum),
        }
        return res

    @classmethod
    def getRecordLevels(cls, record):
        return dict(id=record.get('level_id'), title=record.get('level__name'))

    def makeProdOrderFromRequest(self, request):

        request = DSRequest(request=request)
        data = request.get_data()
        _data = data.copy()
        setAttr(_data, 'user', request.user)

        self.routing_ext.make_routing(data=_data)
        launch_ids = self.production_ext.make_production_order(data=_data)

        self.production_ext.grouping1(launch_ids=launch_ids)
        self.production_ext.fill_locations_sector_ready(launch_ids=list(map(lambda x: x.id, Launches.objects.filter(id__in=launch_ids))), user=request.user)

        self.production_ext.batch_stack.clear()
        return data

    def deleteProdOrderFromRequest(self, request):
        request = DSRequest(request=request)
        data = request.get_data()
        _data = data.copy()
        setAttr(_data, 'user', request.user)
        self.production_ext.delete_production_order(data=_data)

        routing_ext = Routing_ext()
        routing_ext.clean_routing(data=_data)
        return data

    def refreshRowsProdOrderFromRequest(self, request):
        from kaf_pas.planing.models.production_order_per_launch import Production_order_per_launch

        request = DSRequest(request=request)

        data = request.get_data()
        records = data.get('records')
        perLaunch = data.get('perLaunch')

        if perLaunch is True:
            model = Production_order_per_launch
        else:
            model = Production_order

        if isinstance(records, list) and len(records) > 0:
            res_ids = []

            for record in records:
                res_ids = list(map(lambda x: (x.id, x.level), model.tree_objects.get_descendants(id=record.get('id_f'), child_id='id_f', order_by_clause='order by level asc')))

            self.production_ext.refreshRowsProdOrder(
                res_ids=res_ids,
                model=model,
                user=request.user
            )

        return data

    def groupingFromRequest(self, request):
        request = DSRequest(request=request)
        data = request.get_data()

        location_id = data.get('location_id')
        launch_id = data.get('launch_id')

        self.production_ext.grouping(location_id=location_id, launch_id=launch_id)

        return data

    def unGroupingFromRequest(self, request):
        request = DSRequest(request=request)
        data = request.get_data()

        location_id = data.get('location_id')
        launch_id = data.get('launch_id')

        self.production_ext.ungrouping(location_id=location_id, launch_ids=[launch_id] if launch_id else None)

        return data

    def lookupFinishStatusFromRequest(self, request):
        from isc_common.models.standard_colors import Standard_colors

        request = DSRequest(request=request)
        data = request.get_data()
        color = data.get('color__color')
        launch__code = data.get('launch__code')

        res = dict()
        if color is not None:
            res = model_2_dict(Standard_colors.objects.get(color=color))

        if launch__code is not None:
            res = model_2_dict(Launches.objects.get(code=launch__code))

        return res


class Production_order(AuditModel):
    from kaf_pas.planing.models.status_operation_types import Status_operation_types
    from kaf_pas.planing.models.operation_refs import Operation_refsManager

    arranges_exucutors = ArrayField(BigIntegerField(), default=list)
    child_launches = ArrayField(BigIntegerField(), default=list)
    cnt_opers = PositiveIntegerField()
    creator = ForeignKeyProtect(User, related_name='Production_order_creator')
    date = DateTimeField(default=None)
    demand_codes_str = CodeField()
    demand_ids = ArrayField(BigIntegerField(), default=list)
    description = TextField(null=True, blank=True)
    edizm_arr = ArrayField(CodeField(null=True, blank=True), default=list)
    exucutors = ArrayField(BigIntegerField(), default=list)
    exucutors_old = ArrayField(BigIntegerField(), default=list)
    id_f = BigIntegerField()
    isDeleted = BooleanField()
    isFolder = BooleanField()
    item = ForeignKeyProtect(Item, related_name='Production_order_item')
    launch = ForeignKeyCascade(Launches)
    location_ids = ArrayField(BigIntegerField(), default=list)
    location_ids_old = ArrayField(BigIntegerField(), default=list)
    location_sector_ids = ArrayField(BigIntegerField(), default=list)
    location_sectors_full_name = ArrayField(TextField(), default=list)
    location_status_colors = JSONFieldIVC()
    location_status_ids = JSONFieldIVC()
    location_statuses = JSONFieldIVC()
    location_values_made = JSONFieldIVC()
    locations_sector_full_name = JSONFieldIVC()
    location_sectors_ready = JSONFieldIVC()
    max_level = SmallIntegerField()
    num = CodeField()
    opertype = ForeignKeyProtect(Operation_types, related_name='Production_order_opertype')
    parent_id = BigIntegerField(null=True, blank=True)
    parent_item = ForeignKeyProtect(Item, null=True, blank=True, related_name='Production_order_parent_item')
    parent_item_ids = ArrayField(BigIntegerField(), default=list)
    props = Operation_refsManager.props()
    status = ForeignKeyProtect(Status_operation_types)
    value1_sum = ArrayField(DecimalField(decimal_places=4, max_digits=19))
    value_made = DecimalField(verbose_name='Количество  Выпущено', decimal_places=4, max_digits=19, null=True, blank=True)
    value_odd = DecimalField(verbose_name='Количество  Выпущено', decimal_places=4, max_digits=19)
    value_start = DecimalField(verbose_name='Количество Запущено', decimal_places=4, max_digits=19, null=True, blank=True)
    value_sum = DecimalField(verbose_name='Количество по документации', decimal_places=4, max_digits=19)

    objects = Production_orderManager()
    tree_objects = TreeAuditModelManager()

    started = Status_operation_types.objects.get(code='started')

    @classmethod
    def all_childs(cls, id):
        from kaf_pas.planing.models.production_order_opers import Production_order_opers
        return Production_order_opers.objects.filter(parent_id=id, opertype__code=DETAIL_OPERS_PRD_TSK).alive().order_by('production_operation_num')

    def __str__(self):
        return f'\nid: {self.id}, ' \
               f'\nid_f: {self.id_f}, ' \
               f'\nparent_id: {self.parent_id}, ' \
               f'\ndate: {DateTimeToStr(self.date)}, ' \
               f'\nnum: {self.num}, ' \
               f'\ndescription: {self.description}, ' \
               f'\nopertype: [{self.opertype}], ' \
               f'\nisFolder: {self.isFolder}, ' \
               f'\ncreator: [{self.creator}], ' \
               f'\nlocation_ids: {self.location_ids}, ' \
               f'\nlocation_ids_old: {self.location_ids_old}, ' \
               f'\narranges_exucutors: {self.arranges_exucutors}, ' \
               f'\nexucutors: {self.exucutors}, ' \
               f'\nstatus: [{self.status}], ' \
               f'\nlaunch: [{self.launch}], ' \
               f'\nedizm: [{self.edizm_arr}], ' \
               f'\nitem: [{self.item}], ' \
               f'\nparent_item: [{self.parent_item}], ' \
               f'\nparent_items: {self.parent_item_ids}, ' \
               f'\ncnt_opers: {self.cnt_opers}, ' \
               f'\nvalue_sum: {self.value_sum},' \
               f'\nvalue1_sum: {self.value1_sum},' \
               f'\nvalue_start: {self.value_start},' \
               f'\nvalue_made: {self.value_made},' \
               f'\nvalue_odd: {self.value_odd}, ' \
               f'\nprops: {self.props},'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Заказы на производство'
        managed = False
        # db_table = 'planing_production_order_view'
        db_table = 'planing_production_order_tbl'
