import logging
from datetime import datetime

from django.conf import settings
from django.db import transaction, connection
from django.db.models import Count, F
from django.forms import model_to_dict

from events.events_manager import Event
from isc_common import Stack, setAttr, delAttr, StackElementNotExist, StackWithId, Wrapper, delNonePropFromDict, delZeroPropFromDict
from isc_common.bit import TurnBitOn
from isc_common.common import blinkString, uuid4, new, blue, new_man, in_production, red, sht, closed, doing, to_H, green, black
from isc_common.common.functions import ExecuteStoredProc, delete_dbl_spaces
from isc_common.datetime import StrToDate, DateToStr, DateTimeToStr
from isc_common.json import JsonToStr, StrToJson
from isc_common.number import compare_2_dict, Set, flen, DecimalToStr, ToDecimal, model_2_dict, ToNumber, ToInt
from isc_common.progress import managed_progreses, ProgressDroped, progress_deleted, managed_progress
from isc_common.ws.webSocket import WebSocket
from kaf_pas.ckk.models.ed_izm import Ed_izm
from kaf_pas.planing.models.rouning_ext import Routing_ext
from kaf_pas.planing.operation_typesStack import DETAIL_OPERS_PRD_TSK
from kaf_pas.production.models.launches_ext import Launches_ext

logger = logging.getLogger(__name__)


class Launch_pair:
    def __init__(self, child, parent):
        from kaf_pas.production.models.launches import Launches

        if isinstance(child, int):
            self.child = Launches.objects.get(id=child)
        elif isinstance(child, Launches):
            self.child = child
        else:
            raise Exception('child must be int or Launches')

        if isinstance(parent, int):
            self.parent = Launches.objects.get(id=parent)
        elif isinstance(parent, Launches):
            self.parent = parent
        else:
            raise Exception('parent must be int or Launches')

    def __str(self):
        return f'child: [{self.child}], parent: [{self.parent}]'


class Launch_pairs(Stack):
    def get_parents(self):
        res = set()
        for item in self.stack:
            for item1 in item:
                res.add(item1.parent)

        return list(res)

    def get_parent_ids(self):
        return [item.id for item in self.get_parents()]

    def get_childs(self, parent):
        res = set()

        for items in self.stack:
            for item in items:
                if item.child.status.id == settings.PROD_OPERS_STACK.ROUTERROR.id:
                    raise Exception(f'Запуск {item.child.code} от {DateToStr(item.child.date)} имеет статус {item.child.status.name} и не может быть включен в задания на производство, исправьте либо удалите его.')

            res1 = [i.child for i in items if i.parent == parent and i.child.status not in [
                settings.PROD_OPERS_STACK.IN_PRODUCTION,
            ]]
            for r in res1:
                res.add(r)
        return list(res)

    def get_child_ids(self, parent):
        return [item.id for item in self.get_childs(parent=parent)]


class User_ready_struct(Wrapper):
    id = None
    id_f = None
    isFolder = None
    item_name = None
    location_ids = None
    location_sector_ids = None
    stack = None
    table_name_tbl = None

    def __str__(self):
        # return f'id: {self.id}, id_f: {self.id_f}, location_ids: {self.location_ids}, stack: {self.stack}, table_name_tbl: {self.table_name_tbl}'
        return f'id: {self.id}, id_f: {self.id_f}, location_ids: {self.location_ids}, table_name_tbl: {self.table_name_tbl}'


class User_ready_Stack(StackWithId):
    def push(self, item, logger=None):

        if not isinstance(item, dict):
            raise Exception(f'{item} must be dict')

        try:
            _item = self.find_one(item.get(self.id))
            _item.get('location_sectors_ready').update(**item.get('location_sectors_ready'))

            if isinstance(logger, logging.Logger):
                logger.debug(f'self.stack.updated: {_item}')
        except StackElementNotExist:
            self.stack.append(item)
            if isinstance(logger, logging.Logger):
                logger.debug(f'self.stack.append: {item}')
                logger.debug(f'self.stack.size: {self.size()}')

            if isinstance(logger, logging.Logger):
                logger.debug(f'size stack: {len(self.stack)}')

            return True


class RecordAttrs:
    def __init__(self, percents, status__name, status__color, status_id, location_sectors_full_name, location_sectors_ready, item__STMP_1__value_str, launch__code, value1_sum, value_made, value1_sum_len, percents_str=None):
        self.item__STMP_1__value_str = item__STMP_1__value_str
        self.launch__code = launch__code
        self.location_sectors_full_name = location_sectors_full_name
        self.location_sectors_ready = location_sectors_ready
        self.percents = percents
        self.percents_str = percents_str
        self.status__color = status__color
        self.status__name = status__name
        self.status_id = status_id
        self.value1_sum = value1_sum
        self.value1_sum_len = value1_sum_len
        self.value_made = value_made


class Element:
    def __init__(self, record, level, parent_mul, has_color, has_launched, process, color_id=None, childs=None, enabled=None, absorption_operation=None, props=0):
        self.record = record
        self.record_dict = model_2_dict(record)
        self.level = level
        self.parent_mul = parent_mul
        self.color_id = color_id
        self.has_color = has_color
        self.has_launched = has_launched
        self.enabled = enabled
        self.childs = childs
        self.process = process
        self.absorption_operation = absorption_operation
        self.props = props

    @property
    def rec(self):
        from kaf_pas.production.models.launches import Launches

        delAttr(self.record_dict, 'value_made')
        if isinstance(self.childs, list):
            setAttr(self.record_dict, 'childs', list(map(lambda x: x.id, self.childs)))

        if Launches.objects.get(id=self.record_dict.get('launch_id')).parent is not None:
            setAttr(self.record_dict, 'launch_incom_id', self.record_dict.get('launch_id'))

        setAttr(self.record_dict, 'enabled', self.enabled)
        setAttr(self.record_dict, 'has_color', self.has_color)
        setAttr(self.record_dict, 'color_id', self.color_id)
        setAttr(self.record_dict, 'has_launched', self.has_launched)
        setAttr(self.record_dict, 'id_real', self.record.id)
        setAttr(self.record_dict, 'level', self.level)
        setAttr(self.record_dict, 'parent_mul', self.parent_mul)
        setAttr(self.record_dict, 'process', self.process)
        setAttr(self.record_dict, 'props', self.props)
        if not isinstance(self.record_dict.get('value1_sum'), list):
            setAttr(self.record_dict, 'value1_sum', [self.record_dict.get('value1_sum')])
        return self.record_dict


class HashableProdOrder:
    def __init__(self, id, launch_id, isFolder=None, id_f=None):
        from kaf_pas.production.models.launches import Launches

        self.id = id
        self.id_f = id_f
        self.isFolder = isFolder
        self.launch = Launches.objects.get(id=launch_id)

    def __hash__(self):
        return hash(f'{self.id}_{self.launch.id}')

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.id == other.id and self.launch.id == other.launch.id


class ProductionOrderStack(Stack):
    def push(self, item, exists_function=None, logger=None):
        if super().push(item=item, exists_function=exists_function, logger=logger):
            key = f'ProductionOrderStack_{item[0].id}'
            settings.LOCKS.acquire(key)

    def lock_release(self):
        for item in self.stack:
            key = f'ProductionOrderStack_{item[0].id}'
            settings.LOCKS.release(key)


class ProductionOrderErrorStack(Stack):
    def push(self, item, error, exists_function=None, logger=None):

        if not isinstance(error, str):
            raise Exception(f'{error} must be str.')

        try:
            item_error = self.find_one(lambda x: x[0].get('id') == item.get('id'))
            item_error[1].append(error)
        except StackElementNotExist:
            super().push(item=(item, [error]), exists_function=exists_function, logger=logger)

    def has_not_error(self, item):
        return not self.exists(lambda x: x[0].id == item.id)


class Operation_executor_qty:
    def __init__(self, executor, qty, message=None):
        self.executor = executor
        self.qty = qty

    def __str__(self):
        return f'executor : {self.executor}, qty: {self.qty}'


class Operation_executor_stack(Stack):
    len = 0

    def push(self, item, exists_function=None, logger=None):
        from isc_common.auth.models.user import User
        if not isinstance(item.executor, User):
            raise Exception('executor mast be User instance')

        try:
            executor_qty = self.find_one(lambda _item: _item.executor == item.executor)
            executor_qty.qty += item.qty
            self.len += item.qty

            if logger is not None:
                logger.debug(f'operation_executor_qty: {executor_qty}')

        except StackElementNotExist:
            operation_executor_qty = Operation_executor_qty(executor=item.executor, qty=item.qty)
            if logger is not None:
                logger.debug(f'operation_executor_qty: {operation_executor_qty}')

            super().push(Operation_executor_qty(executor=item.executor, qty=item.qty))
            self.len += 1


class OperationEvent(Event):
    def send_message(self, message=None, users_array=None, progress=None, _len=None):
        from isc_common.auth.models.user import User
        if isinstance(users_array, User):
            users_array = [users_array]
        super().send_message(message=message, users_array=users_array, progress=progress)

    def send_message1(self, operation_executor_stack: Operation_executor_stack, progress=None):
        for operation_executor_messages in operation_executor_stack.stack:
            for message in operation_executor_messages.messages.stack:
                super().send_message(message=message, users_array=[operation_executor_messages.executor], progress=progress)


class Operation_executor_messages:
    def __init__(self, executor, message):
        self.executor = executor
        self.messages = Stack([message])


class OperationPlanItem:
    item_id = None
    launch_ids = None
    sum = None
    value = None

    # Определить цех ресурса
    def get_resource_workshop(self, operation_resources):
        from kaf_pas.ckk.models.locations import Locations
        from django.conf import settings

        res_set = set()
        for operation_resource in operation_resources:
            for location in Locations.objects_tree.get_parents(id=operation_resource.location.id, child_id='id', include_self=False):
                if location.props.isWorkshop == True:
                    res, _ = settings.OPERS_STACK.NOT_UNDEFINED_WORKSHOP(location)
                    res_set.add(res.location.id)

        if len(res_set) == 0:
            raise Exception('Не обнаружен цех, с признаком "Уровень цеха"')
        lst = list(res_set)
        return list(Locations.objects.filter(id__in=lst))

    def get_locations_users_query(self, locations):
        from kaf_pas.ckk.models.locations_users import Locations_users
        from isc_common.common import blinkString

        res_set = set()
        exeptions = Stack()
        for location in locations:
            locations_users_query = Locations_users.objects.filter(location=location, parent=None, props=Locations_users.props.resiver_production_order)
            if locations_users_query.count() == 0:
                exeptions.push(blinkString(text=f'Не обнаружен ответственный исполнитель на : {location.full_name}', bold=True, color=red, blink=False))
            else:
                for locations_users in locations_users_query:
                    res_set.add(locations_users.id)

        if exeptions.size() > 0:
            raise Exception('<br>'.join(exeptions))

        res = list(Locations_users.objects.filter(id__in=list(res_set)))
        return res

    def __init__(self, *args, **kwargs):
        # from kaf_pas.ckk.models.item import Item
        from kaf_pas.production.models.resource import Resource
        from kaf_pas.production.models.operations_item import Operations_item
        from kaf_pas.production.models.operation_resources import Operation_resources
        from kaf_pas.production.models.operation_material import Operation_material
        from kaf_pas.ckk.models.locations import Locations
        from django.db import connection
        from django.conf import settings
        from kaf_pas.ckk.models.item import Item

        class OperationsItem:
            def __init__(self, operation_item):
                operation_resources = Operation_resources.objects.get(operationitem=operation_item)
                self.operation_item = operation_item
                self.operation_resource = operation_resources
                self.ed_izm = operation_item.ed_izm
                self.num = operation_item.num
                self.operation = operation_item.operation
                self.color = operation_item.color
                self.old_num = operation_item.old_num
                self.qty = operation_item.qty

                self.location_fin = operation_resources.location_fin

                self.resource = operation_resources.resource
                if self.resource is None:
                    self.resource, _ = Resource.objects.get_or_create(location=self.operation_resource.location, code='none')

                self.resource_fin = operation_resources.resource_fin
                if self.resource_fin is None and self.operation_resource.location_fin is not None:
                    self.resource_fin, _ = Resource.objects.get_or_create(location=self.operation_resource.location_fin, code='none')

                self.operation_materials = Stack([operation_material for operation_material in Operation_material.objects.filter(operationitem=operation_item)])

            def __str__(self):
                return f'''\n\noperation_item: [\n\n{self.operation_item}] \n operation_resource: [{self.operation_resource}] \n operation_materials: [[{", ".join([operation_material for operation_material in self.operation_materials])}]]'''

        class LaunchSumValue:
            sum = None

            def __init__(self, sum_value, sum_value1, edizm_id, launch_id, item_id):
                from kaf_pas.production.models.launches import Launches

                self.sum_value = sum_value
                self.sum_value1 = sum_value1
                self.edizm_id = edizm_id
                self.item_id = item_id
                self.launch = Launches.objects.get(id=launch_id)

            def __str__(self):
                return f'sum: {self.sum}, launch: [{self.launch}]'

        class LaunchSumValues(Stack):
            def __init__(self, item, launch_ids):
                super().__init__()

                self.stack = []
                with connection.cursor() as cursor:
                    sql_str = '''select sum(distinct pov.value),
                                           sum(distinct pov1.value),
                                           pol.launch_id,
                                           pov.edizm_id
                                   from planing_operation_launches as pol
                                             join planing_operations as po on po.id = pol.operation_id
                                             join planing_operation_item as poit on po.id = poit.operation_id
                                             join planing_operation_value pov on pov.operation_id = po.id
                                             join planing_operation_value pov1 on pov1.operation_id = po.id
                                   where pol.launch_id in %s
                                      and po.opertype_id = %s
                                      and poit.item_id = %s
                                      and is_bit_on(pov.props::integer, 0) = false
                                      and is_bit_on(pov1.props::integer, 0) = true
                                    group by pol.launch_id, pov.edizm_id'''

                    cursor.execute(sql_str, [launch_ids, settings.OPERS_TYPES_STACK.ROUTING_TASK.id, item.id])
                    rows = cursor.fetchall()

                    for row in rows:
                        sum_value, sum_value1, launch_id, edizm_id = row
                        launchSumValue = LaunchSumValue(sum_value=sum_value, sum_value1=sum_value1, edizm_id=edizm_id, launch_id=launch_id, item_id=item.id)
                        self.push(launchSumValue)

            def __str__(self):
                return '\n\n'.join([f'[{elem}]' for elem in self.stack])

        if len(kwargs) == 0:
            raise Exception(f'{self.__class__.__name__} kwargs is empty')

        for k, v in kwargs.items():
            setattr(self, k, v() if callable(v) else v)

        if isinstance(self.item_id, int):
            self.item = Item.objects.get(id=self.item_id)

        if self.item is None:
            raise Exception('self.item not determined')

        self.operations_item = Stack([OperationsItem(operation_item) for operation_item in Operations_item.objects.filter(item=self.item).exclude(deleted_at__isnull=False).order_by('num')])

        self.resources_location_fin_arr = [(operation_item.resource, operation_item.resource_fin, operation_item.location_fin) for operation_item in self.operations_item]

        # operation_item = self.operations_item.stack[0].operation_item
        oit_lst = [a.operation_item for a in self.operations_item]
        operation_resources = [operation_resources for operation_resources in Operation_resources.objects.filter(operationitem__in=oit_lst)]

        top_locations = self.get_resource_workshop(operation_resources=operation_resources)
        operation_locations = list(map(lambda x: Locations.objects.get(id=x), set(list(map(lambda x: x.location.id, operation_resources)))))

        if settings.LOCATION_LEVEL == 'LOCATION':
            self.locations_users = [location_user for location_user in self.get_locations_users_query(locations=operation_locations)]
        elif settings.LOCATION_LEVEL == 'TOP_LOCATION':
            self.locations_users = [location_user for location_user in self.get_locations_users_query(locations=top_locations)]
        else:
            raise Exception('Not have LOCATION_LEVEL')

        from kaf_pas.production.models.operation_executor import Operation_executor
        production_operations = map(lambda x: x.operation, self.operations_item)
        self.operation_executors = list(map(lambda x: x.user, Operation_executor.objects.filter(operation__in=production_operations).distinct()))

        self.launchSumValues = LaunchSumValues(item=self.item, launch_ids=self.launch_ids)

    def __str__(self):
        # return f'item: {self.item} \n value_sum: {self.value}\n value_per_one: {self.value1}\n\n launchSumValues: [\n{self.launchSumValues.stack}\n] \n\n operations_item: [\n{", ".join([f"[{elem}]" for elem in self.operations_item])}]'
        return f'item: {self.item} \n value_sum: {self.value}\n  launchSumValues: [\n{self.launchSumValues.stack}\n] \n\n operations_item: [\n{", ".join([f"[{elem}]" for elem in self.operations_item])}]'


class Production_ext:
    routing_ext = Routing_ext()

    _res = []

    edizm_shtuka = Ed_izm.objects.get(code=sht)
    batch_stack = Stack()

    def delete_underscore_element(self, data):
        if not isinstance(data, dict):
            raise Exception('data must be dict')

        res = dict()
        for key, value in data.items():
            if str(key).find('_', 0, 1) == -1:
                setAttr(res, key, value)
        return res

    def get_launches(self, operations, res=None, launch=None):
        from kaf_pas.accounting.models.buffers import Buffers
        from kaf_pas.planing.models.production_order_values_ext import Production_orderWrapper
        from kaf_pas.production.models.launch_item_prod_order_per_launch_view import Launch_item_prod_order_per_launch_view
        from kaf_pas.production.models.launch_item_refs import Launch_item_refs
        from kaf_pas.production.models.launches import Launches
        from kaf_pas.production.models.launches_view import Launches_view
        from kaf_pas.production.models.launches_view import Launches_viewManager

        if res is None:
            res = []

        launch_flt = []
        if launch is not None:
            launch_flt = launch.parent
            if launch_flt is not None:
                launch_flt = [launch_flt]
            else:
                launch_flt = [launch]
                launch_flt.extend(list(Launches.objects.filter(parent=launch)))

        for operation in operations:
            record_0 = Production_orderWrapper(**operation)

            if record_0.production_operation_num == 1:
                launches = set(map(lambda x: x.launch.id, Launch_item_refs.tree_objects.get_descendants(id=record_0.item.id)))
                for launche_view_item in Launches_view.objects.filter(id__in=launches):
                    record = Launches_viewManager.getRecord(launche_view_item)

                    for launch_item_order in Launch_item_prod_order_per_launch_view.objects.filter(
                            item=record_0.item,
                            launch_id=launche_view_item.id
                    ):
                        if launch_item_order.qty_odd > 0:
                            setAttr(record, 'value_odd', blinkString(DecimalToStr(launch_item_order.qty_odd), blink=False, color=green, bold=True))
                            setAttr(record, 'value_odd_f', ToNumber(launch_item_order.qty_odd))
                            res.append(record)
                        # else:
                        #     res.append(setAttr(record, 'value_odd', blinkString(DecimalToStr(launch_item_order.qty_odd), blink=True, color=red, bold=True)))
            else:
                bufer_query = Buffers.objects.filter(item=record_0.item, last_operation=record_0.childs[record_0.production_operation_num - 2].production_operation)
                if len(launch_flt) > 0:
                    bufer_query = bufer_query.filter(launch__in=launch_flt)

                for buffers_item in bufer_query:
                    value_odd = buffers_item.value

                    if value_odd > 0:
                        record = Launches_viewManager.getRecord(Launches_view.objects.get(id=buffers_item.launch.id))
                        setAttr(record, 'value_odd', blinkString(DecimalToStr(value_odd), blink=False, color=green, bold=True))
                        setAttr(record, 'value_odd_d', ToNumber(value_odd))
                        res.append(record)
        return res

    def get_excutors_operation(self, parent_id):
        with connection.cursor() as cursor:
            cursor.execute('''select distinct clu.user_id, poop.id
                                from planing_production_order_opers_view poop
                                         join ckk_locations_users clu on clu.location_id = poop.location_id
                                where poop.parent_id = %s
                                  and poop.production_operation_id not in (select operation_id from production_operation_executor)
                                union
                                select distinct prdex.user_id, poop.id
                                from planing_production_order_opers_view poop
                                         join production_operation_executor prdex on prdex.operation_id = poop.production_operation_id
                                where poop.parent_id = %s''', [parent_id, parent_id])
            rows = cursor.fetchall()
            return rows

    def get_excutors(self, parent_id):
        from isc_common.auth.models.user import User
        executors = self.get_excutors_operation(parent_id=parent_id)
        executors = list(set(list(map(lambda x: x[0], executors))))
        executors = User.objects.filter(id__in=executors)
        return executors

    def refresh_production_order_executors(self, parent_id):
        from kaf_pas.planing.models.production_order import Production_order
        from kaf_pas.planing.models.production_order_per_launch import Production_order_per_launch
        from kaf_pas.planing.models.production_order import Production_orderManager

        for executor in self.get_excutors(parent_id=parent_id):
            Production_orderManager.refreshRows(ids=parent_id, user=executor, model=Production_order)
            Production_orderManager.refreshRows(ids=parent_id, user=executor, model=Production_order_per_launch)

    def start(self, qty, _data, user, operation_executor_stack, launch, model, lock=True):
        from django.conf import settings
        from isc_common.common import new
        from isc_common.common import restarted
        from isc_common.common.functions import ExecuteStoredProc
        from kaf_pas.planing.models.operation_launches import Operation_launches
        from kaf_pas.planing.models.operation_refs import Operation_refs
        from kaf_pas.planing.models.operation_value import Operation_value
        from kaf_pas.planing.models.operations import Operations
        from kaf_pas.planing.models.operations_view import Operations_view
        from kaf_pas.planing.models.production_order import Production_orderManager

        key = f'''start_{_data.get('id')}'''

        # location_ids = Production_orderQuerySet.get_user_locations(user=user)

        if lock:
            settings.LOCKS.acquire(key)
        try:
            value_made = ExecuteStoredProc('get_max_value_made', [_data.get('id'), _data.get('launch_id')])

            qty = ToDecimal(qty)
            if value_made > qty:
                if lock:
                    settings.LOCKS.release(key)
                raise Exception('Количество выпуска больше введенной суммы. Введите с учетом выпущенного.')

            parent = Operations.objects.get(id=_data.get('id'))

            operation_refs = Operation_refs.objects.filter(
                parent=parent,
                child__opertype=settings.OPERS_TYPES_STACK.LAUNCH_TASK
            )

            if operation_refs.count() > 0:
                if qty == 0:
                    Operation_value.objects.filter(operation=operation_refs[0].child).delete()
                    Operation_launches.objects.filter(operation=operation_refs[0].child).delete()
                    parent.status = settings.OPERS_TYPES_STACK.PRODUCTION_TASK_STATUSES.get(new)
                    operation_refs.delete()

                else:
                    res, created = Operation_value.objects.update_or_create(operation=operation_refs[0].child, defaults=dict(value=qty))
                    Operation_launches.objects.get_or_create(
                        operation=operation_refs[0].child,
                        launch=Operations_view.objects.get(id=operation_refs[0].child.id).launch
                    )
                    parent.status = settings.OPERS_TYPES_STACK.PRODUCTION_TASK_STATUSES.get(restarted)

                parent.save()

                for executor in self.get_excutors(parent_id=parent.id):
                    operation_executor_stack.push(
                        Operation_executor_qty(executor=executor, qty=0),
                        logger
                    )

                # if qty != 0:
                setAttr(_data, 'value_start', qty)
                # self._res.append(_data)

            else:
                if qty == 0:
                    if lock:
                        settings.LOCKS.release(key)
                    return None

                res = Operations.objects.create(
                    opertype=settings.OPERS_TYPES_STACK.LAUNCH_TASK,
                    date=datetime.now(),
                    status=settings.OPERS_TYPES_STACK.LAUNCH_TASK_STATUSES.get(new),
                    creator=user
                )

                parent.status = settings.OPERS_TYPES_STACK.PRODUCTION_TASK_STATUSES.get('started')
                parent.save()

                Operation_refs.objects.create(parent=parent, child=res)
                edizm_id = _data.get('edizm_id')
                if edizm_id is None:
                    edizm_id = self.edizm_shtuka.id

                Operation_value.objects.create(operation=res, edizm_id=edizm_id, value=qty)
                Operation_launches.objects.get_or_create(operation=res, launch=launch if launch.parent is None else launch.parent)

                executors = self.get_excutors(parent_id=parent.id)
                self.set_executors(
                    executors=list(executors),
                    operation=parent,
                    operation_executor_stack=operation_executor_stack,
                    user=user,
                    send=False
                )

                setAttr(_data, 'value_start', qty)
                # self._res.append(_data)

            # self.updateModelRow(
            #     id=parent.id,
            #     launch_id=_data.get('launch_id'),
            #     location_ids=location_ids,
            #     model=model,
            #     status=parent.status,
            #     user=user,
            # )
            Production_orderManager.update_redundant_planing_production_order_table(ids=parent, model=model, user=user)

            if lock:
                settings.LOCKS.release(key)

            return _data
        except Exception as ex:
            self._res.clear()
            if lock:
                settings.LOCKS.release(key)
            raise ex

    def set_executors(self, executors, operation, operation_executor_stack, user, send=True):
        from kaf_pas.planing.models.operation_executor import Operation_executor
        from kaf_pas.planing.models.production_order import Production_orderManager

        cnt = 0
        if isinstance(executors, list):
            # Раннее назначенные исполнителя для данной операции
            for executor in executors:
                operation_executor, created = Operation_executor.objects.get_or_create(operation=operation, executor=executor)

                if user.id != executor.id:
                    operation_executor_stack.push(
                        Operation_executor_qty(executor=operation_executor.executor, qty=1),
                        logger
                    )
                cnt += 1

        # От лица запускающего операцию отправляем
        if cnt > 0 and send:
            try:
                operation_executor = Operation_executor.objects.get(operation=operation, executor=user)
                operation_executor.props |= Operation_executor.props.rearrange
                operation_executor.save()

                Production_orderManager.update_redundant_planing_production_order_table(operation.id, user=user)
            except Operation_executor.DoesNotExist:
                pass

    def rec_operation(self,
                      description,
                      item,
                      operation,
                      launch,
                      operation_item,
                      opertype,
                      status,
                      user,
                      props=0,
                      ):
        from datetime import datetime
        from kaf_pas.ckk.models.item import Item
        from kaf_pas.planing.models.operation_item import Operation_item
        from kaf_pas.planing.models.operation_launches import Operation_launches
        from kaf_pas.planing.models.operation_material import Operation_material
        from kaf_pas.planing.models.operation_operation import Operation_operation
        from kaf_pas.planing.models.operation_refs import Operation_refs
        from kaf_pas.planing.models.operation_resources import Operation_resources
        from kaf_pas.planing.models.operations import Operations
        from kaf_pas.production.models.launches import Launches

        if isinstance(launch, int):
            launch = Launches.objects.get(id=launch)

        if isinstance(item, int):
            item = Item.objects.get(id=item)

        if isinstance(operation, int):
            operation = Operations.objects.get(id=operation)

        production_order_operation_opers = Operations.objects.create(
            date=datetime.now(),
            opertype=opertype,
            status=status,
            creator=user,
            description=description,
            editing=False,
            deliting=False
        )

        operation_launches = Operation_launches.objects.create(
            operation=production_order_operation_opers,
            launch=launch
        )
        logger.debug(f'Created operation_launches :  {operation_launches}')

        if operation_item.resource is not None:
            operation_resources = Operation_resources.objects.create(
                operation=production_order_operation_opers,
                resource=operation_item.resource,
                resource_fin=operation_item.resource_fin,
                location_fin=operation_item.location_fin
            )
            logger.debug(f'Created operation_resources :  {operation_resources}')

        for operation_material in operation_item.operation_materials:
            operation_material = Operation_material.objects.create(
                operation=production_order_operation_opers,
                material=operation_material.material,
                material_askon=operation_material.material_askon,
                edizm=operation_material.edizm,
                qty=operation_material.qty,
            )
            logger.debug(f'Created operation_material :  {operation_material}')

        operation_operation = Operation_operation.objects.create(
            operation=production_order_operation_opers,
            production_operation=operation_item.operation,
            color=operation_item.color,

            ed_izm=operation_item.ed_izm,
            num=operation_item.num,
            qty=operation_item.qty,
            creator=user,
            props=props
        )
        logger.debug(f'Created operation_operation :  {operation_operation}')

        operation_item, created = Operation_item.objects.get_or_create(
            operation=production_order_operation_opers,
            item=item,
        )
        if created:
            logger.debug(f'Created operation_item :  {operation_item}')

        operation_refs = Operation_refs.objects.create(
            parent=operation,
            child=production_order_operation_opers,
            props=Operation_refs.props.product_order_routing,
        )
        logger.debug(f'Created operation_refs :  {operation_refs}')

        return production_order_operation_opers

    def rec_operations(self, launch, status, operationPlanItem, operation, opertype, description, user):

        for operation_item in operationPlanItem.operations_item:
            self.rec_operation(
                launch=launch,
                status=status,
                operation_item=operation_item,
                item=operationPlanItem.item,
                operation=operation,
                opertype=opertype,
                description=description,
                user=user
            )

    def rec_item(self,
                 item_id,
                 launch_childs_ids,
                 launch_parent,
                 user,
                 operation_executor_stack,
                 route_opers_lunch,
                 description,
                 status_name=new
                 ):
        from datetime import datetime
        from django.conf import settings
        from kaf_pas.planing.models.operation_executor import Operation_executor
        from kaf_pas.planing.models.operation_item import Operation_item
        from kaf_pas.planing.models.operation_launches import Operation_launches
        from kaf_pas.planing.models.operation_refs import Operation_refs
        from kaf_pas.planing.models.operation_resources import Operation_resources
        from kaf_pas.planing.models.operation_value import Operation_value
        from kaf_pas.planing.models.operations import Operations
        from kaf_pas.planing.models.production_order import Production_order
        from kaf_pas.planing.models.production_order_per_launch import Production_order_per_launch

        route_oparation_item = dict(
            item_id=item_id,
            launch_ids=launch_childs_ids,
            launch_parent_id=launch_parent.id
        )

        operationPlanItem = OperationPlanItem(**route_oparation_item)

        # Головная операция заказа
        production_order_operation = Operations.objects.create(
            date=datetime.now(),
            opertype=settings.OPERS_TYPES_STACK.PRODUCTION_TASK,
            status=settings.OPERS_TYPES_STACK.PRODUCTION_TASK_STATUSES.get(status_name),
            description=description,
            creator=user,
            editing=False,
            deliting=False
        )
        logger.debug(f'Created operation :  {production_order_operation}')

        operation_launches = Operation_launches.objects.create(
            operation=production_order_operation,
            launch=launch_parent
        )
        logger.debug(f'Created operation_launches :  {operation_launches}')

        operation_item = Operation_item.objects.create(
            operation=production_order_operation,
            item=operationPlanItem.item,
        )
        logger.debug(f'Created operation_item :  {operation_item}')

        for launch_child_id in launch_childs_ids:
            for route_oper_lunch in route_opers_lunch:
                if route_oper_lunch[1] == launch_child_id:
                    for route_oper in route_oper_lunch[0]:
                        operation_refs = Operation_refs.objects.create(
                            child=production_order_operation,
                            parent_id=route_oper,
                            props=Operation_refs.props.product_order_routing,
                        )
                        logger.debug(f'Created operation_refs :  {operation_refs}')

        for resources_location_fin in operationPlanItem.resources_location_fin_arr:
            operation_resources, created = Operation_resources.objects.get_or_create(
                operation=production_order_operation,
                resource=resources_location_fin[0],
                resource_fin=resources_location_fin[1],
                location_fin=resources_location_fin[2]
            )
            if created:
                logger.debug(f'Created operation_resources :  {operation_resources}')

        for launchSumValue in operationPlanItem.launchSumValues.stack:
            production_order_operation_launch = Operations.objects.create(
                date=datetime.now(),
                opertype=settings.OPERS_TYPES_STACK.PRODUCTION_DETAIL_SUM_TASK,
                status=settings.OPERS_TYPES_STACK.PRODUCTION_DETAIL_SUM_TASK_STATUSES.get(new),
                creator=user,
                editing=False,
                deliting=False
            )
            logger.debug(f'Created operation :  {production_order_operation}')

            operation_launches = Operation_launches.objects.create(
                operation=production_order_operation_launch,
                launch=launchSumValue.launch
            )
            logger.debug(f'Created operation_launches :  {operation_launches}')

            operation_value = Operation_value.objects.create(
                operation=production_order_operation_launch,
                edizm_id=launchSumValue.edizm_id,
                value=launchSumValue.sum_value
            )
            logger.debug(f'Created operation_value :  {operation_value}')

            operation_value = Operation_value.objects.create(
                operation=production_order_operation_launch,
                edizm_id=launchSumValue.edizm_id,
                value=launchSumValue.sum_value1,
                props=Operation_value.props.perone
            )
            logger.debug(f'Created operation_value :  {operation_value}')

            operation_refs = Operation_refs.objects.create(
                child=production_order_operation_launch,
                parent=production_order_operation,
                props=Operation_refs.props.product_order_routing,
            )
            logger.debug(f'Created operation_refs :  {operation_refs}')

        self.rec_operations(
            launch=launch_parent,
            status=settings.OPERS_TYPES_STACK.PRODUCTION_DETAIL_OPERS_TASK_STATUSES.get(new),
            operationPlanItem=operationPlanItem,
            operation=production_order_operation,
            opertype=settings.OPERS_TYPES_STACK.PRODUCTION_DETAIL_OPERS_TASK,
            description=description,
            user=user
        )

        for location_user in operationPlanItem.locations_users:
            operation_executor, created = Operation_executor.objects.get_or_create(
                operation=production_order_operation,
                executor=location_user.user,
            )
            if created:
                logger.debug(f'Created operation_executor :  {operation_executor}')

            operation_executor_stack.push(
                Operation_executor_qty(executor=location_user.user, qty=1),
                logger
            )

        for operation_executor in operationPlanItem.operation_executors:
            Operation_executor.objects.get_or_create(operation=production_order_operation, executor=operation_executor)
            operation_executor_stack.push(
                Operation_executor_qty(executor=operation_executor, qty=1),
                logger
            )

        Production_order.objects.filter(id=production_order_operation.id).check_state()
        Production_order_per_launch.objects.filter(id=production_order_operation.id).check_state()
        # Production_orderManager.update_redundant_planing_production_order_table(production_order_operation)
        return production_order_operation

    def make_production_order(self, data, batch_mode=False):
        from isc_common.bit import TurnBitOn
        from isc_common.common import blinkString
        from isc_common.datetime import DateToStr
        from isc_common.progress import managed_progress
        from isc_common.progress import progress_deleted
        from isc_common.progress import ProgressDroped
        from kaf_pas.planing.models.production_order import Production_order
        from kaf_pas.planing.models.production_order import Production_orderManager
        from kaf_pas.planing.models.production_order_per_launch import Production_order_per_launch
        from kaf_pas.production.models.launches import Launches
        from kaf_pas.production.models.launches_view import Launches_viewManager

        user = data.get('user')

        if isinstance(user, int):
            from isc_common.auth.models.user import User
            user = User.objects.get(id=user)

        launch_pairs = Launch_pairs()

        launches_head = []
        for launch_id in set(data.get('data')):
            _launch = Launches.objects.get(id=launch_id)
            if _launch.parent is None:
                launches = list(Launches.objects.filter(parent=_launch))
            else:
                launches = [_launch]

            launch_pairs.push([Launch_pair(parent=launch.parent, child=launch) for launch in launches])
            if _launch.parent is None:
                launches_head.append(_launch)
            else:
                launches_head.append(_launch.parent)

        for launch_parent in launch_pairs.get_parents():
            if launch_parent.code != '000':
                if launch_parent.status == settings.PROD_OPERS_STACK.IN_PRODUCTION:
                    continue

            self.batch_stack.clear()
            key = f'OperationsManager.make_production_order_{launch_parent.id}'
            settings.LOCKS.acquire(key)

            launch_childs = launch_pairs.get_childs(parent=launch_parent)
            launch_childs_ids = tuple([launch.id for launch in launch_childs])

            operation_executor_stack = Operation_executor_stack()

            sql_items = '''select poit.item_id
                                 from planing_operation_item as poit
                                   join planing_operation_launches as pol on poit.operation_id = pol.operation_id
                                   join planing_operations as po on po.id = pol.operation_id
                                 where pol.launch_id in %s
                                   and po.opertype_id = %s
                                 group by poit.item_id'''

            sql_items_launch = '''select array_agg(poit_det.operation_id)
                                       from planing_operation_item as poit_det
                                                join planing_operation_launches as pol on poit_det.operation_id = pol.operation_id
                                                join planing_operations as po on po.id = pol.operation_id
                                       where pol.launch_id = %s
                                         and po.opertype_id = %s
                                         and poit_det.item_id = %s
                                       group by pol.launch_id'''

            with connection.cursor() as cursor:

                cursor.execute(f'''select count(*) from ({sql_items}) as s''', [launch_childs_ids, settings.OPERS_TYPES_STACK.ROUTING_TASK.id])
                qty, = cursor.fetchone()
                logger.debug(f'qty: {qty}')

                message = [to_H(f'Создание заданий на производство ({qty} товарных позиций) <p/>')]

                message.extend([blinkString(f'Запуск № {launch.code} от {DateToStr(launch.date)}', blink=False, bold=True, color='blue') for launch in launch_childs])
                message = '<br/>'.join(message)

                import time
                start_time = time.clock()
                with managed_progress(
                        id=f'order_by_prod_launch_{launch_parent.id}_{user.id}',
                        qty=qty,
                        user=user,
                        message=blinkString(text="Проверка наличия ответственных исполнителей в цехах и на участках.", blink=False, color=blue, bold=True),
                        title='Выполнено',
                        props=TurnBitOn(0, 0)
                ) as progress:

                    with transaction.atomic():
                        def except_func():
                            settings.LOCKS.release(key)

                        progress.except_func = except_func
                        with transaction.atomic():
                            cursor.execute(sql_items, [launch_childs_ids, settings.OPERS_TYPES_STACK.ROUTING_TASK.id])
                            rows = cursor.fetchall()
                            # Проверка наличия ответственных исполнителей в цехах
                            for row in rows:
                                item_id, = row

                                route_oparation_item = dict(
                                    item_id=item_id,
                                    launch_ids=launch_childs_ids,
                                    launch_parent_id=launch_parent.id
                                )

                                OperationPlanItem(**route_oparation_item)

                                if progress.step() != 0:
                                    settings.LOCKS.release(key)
                                    raise ProgressDroped(progress_deleted)

                        with transaction.atomic():
                            progress.setContentsLabel(content=message)
                            progress.setQty(qty=qty)
                            for row in rows:
                                item_id, = row

                                # items_4_find = ItemManager.find_item(item_id)

                                route_opers_lunch = []
                                for launch_childs_id in launch_childs_ids:
                                    cursor.execute(sql_items_launch, [launch_childs_id, settings.OPERS_TYPES_STACK.ROUTING_TASK.id, item_id])
                                    rows_lunch = cursor.fetchall()
                                    for row_lunch in rows_lunch:
                                        row_lunch, = row_lunch
                                        route_opers_lunch.append((row_lunch, launch_childs_id))

                                production_order_operation = self.rec_item(
                                    item_id=item_id,
                                    launch_childs_ids=launch_childs_ids,
                                    launch_parent=launch_parent,
                                    user=user,
                                    operation_executor_stack=operation_executor_stack,
                                    route_opers_lunch=route_opers_lunch,
                                    description=data.get('description'),
                                    status_name=new if launch_parent.code != '000' else new_man
                                )

                                self.batch_stack.push(production_order_operation.id)

                                if batch_mode is False:
                                    ExecuteStoredProc('insert_into_planing_production_order_s', [[production_order_operation.id]])
                                    ExecuteStoredProc('insert_into_planing_production_order_per_launch_s', [[production_order_operation.id]])

                                if progress.step() != 0:
                                    Launches_viewManager.fullRows()
                                    settings.LOCKS.release(key)
                                    raise ProgressDroped(progress_deleted)

                                Launches_viewManager.refreshRows(ids=launch_parent.id)
                                Launches_viewManager.refreshRows(ids=launch_childs_ids)

                            launch_parent.status = settings.PROD_OPERS_STACK.IN_PRODUCTION
                            launch_parent.save()

                            for launch_child in launch_childs:
                                launch_child.status = settings.PROD_OPERS_STACK.IN_PRODUCTION
                                launch_child.save()

                                Launches_viewManager.refreshRows(ids=launch_child.id)

                        if batch_mode is True:
                            with transaction.atomic():
                                progress.setContentsLabel(content=blinkString(text="Перенос данных (Общая таблица)", blink=True, color=blue, bold=True))
                                ExecuteStoredProc('insert_into_planing_production_order_s', [self.batch_stack.stack])

                            with transaction.atomic():
                                progress.setContentsLabel(content=blinkString(text="Перенос данных (Таблица по заказам)", blink=True, color=blue, bold=True))
                                ExecuteStoredProc('insert_into_planing_production_order_per_launch_s', [self.batch_stack.stack])

                        with transaction.atomic():
                            progress.setContentsLabel(content=blinkString(text="Обновление исполнителей", blink=True, color=blue, bold=True))

                            Production_orderManager.update_executors(ids=self.batch_stack.stack, model=Production_order, user=user)
                            Production_orderManager.update_executors(ids=self.batch_stack.stack, model=Production_order_per_launch, user=user)
                        settings.LOCKS.release(key)

                    logger.debug(f'operation_executor_stack.len: {operation_executor_stack.len} messages')
                    for operation_executor in operation_executor_stack:
                        settings.EVENT_STACK.EVENTS_PRODUCTION_ORDER_CREATE.send_message(
                            message=blinkString(to_H(f'Вам направлено: {operation_executor.qty} новых заданий на производство.'), bold=True, color=blue, blink=False),
                            users_array=[operation_executor.executor],
                            progress=progress,
                        )
                print(f'make_production_order Time: {time.clock() - start_time}')

        records = launch_pairs.get_parent_ids()
        for parent in launch_pairs.get_parent_ids():
            records.extend([_id for _id in launch_pairs.get_child_ids(parent=parent)])

        Launches_viewManager.refreshRows(ids=records)
        Production_orderManager.fullRows()
        return records

    def delete_production_order(self, data):
        from django.conf import settings
        from django.db import transaction
        from isc_common.bit import TurnBitOn
        from isc_common.common import blinkString
        from isc_common.datetime import DateToStr
        from isc_common.progress import managed_progress
        from isc_common.progress import progress_deleted
        from isc_common.progress import ProgressDroped
        from kaf_pas.planing.models.operation_executor import Operation_executor
        from kaf_pas.planing.models.operation_refs import Operation_refs
        from kaf_pas.production.models.launches import Launches
        from kaf_pas.production.models.launches_view import Launches_viewManager
        from kaf_pas.planing.models.production_order_values_ext import Production_order_values_ext
        from kaf_pas.planing.models.production_order import Production_orderManager
        from kaf_pas.planing.models.operation_launches import Operation_launches
        from kaf_pas.planing.models.operation_operation import Operation_operation
        from kaf_pas.accounting.models.buffers import BuffersManager
        from isc_common.auth.models.user import User

        user = data.get('user')

        launch_ids = data.get('data')
        if not isinstance(launch_ids, list):
            raise Exception('launch_ids must be list')

        launch_ids = list(set(launch_ids))
        production_order_values_ext = Production_order_values_ext()

        if isinstance(user, int):
            user = User.objects.get(id=user)
        elif not isinstance(user, User):
            raise Exception('user must be int or User')

        operation_executor_stack = Operation_executor_stack()

        launch_cnt = len(launch_ids)
        idx = 0
        operation_launch_deleted = 0
        parent_launch_ids = []

        for parent_launch_id in launch_ids:
            parent_launch = Launches.objects.get(id=parent_launch_id)
            if parent_launch.parent is None:
                parent_launch_ids.append(parent_launch.id)

            key = f'OperationsManager.delete_production_order_{parent_launch.id}'
            settings.LOCKS.acquire(key)
            # print(model_to_dict(parent_launch))

            if parent_launch.parent is None:
                child_launches = [launch.id for launch in Launches.objects.filter(parent=parent_launch)]
            else:
                child_launches = [parent_launch]

            operations_launch = Operation_launches.objects.filter(
                operation__opertype=settings.OPERS_TYPES_STACK.PRODUCTION_TASK,
                launch=parent_launch
            )

            operations_launch_cnt = operations_launch.count()
            logger.debug(f'operations_launch.count() = {operations_launch_cnt}')

            with managed_progress(
                    id=f'delete_order_by_prod_launch_{parent_launch.id}_{user.id}',
                    qty=operations_launch_cnt,
                    user=user,
                    message=f'<h3>Удаление заданий на производство, Запуск № {parent_launch.code} от {DateToStr(parent_launch.date)}</h3>',
                    title='Выполнено',
                    props=TurnBitOn(0, 0)
            ) as progress:
                def except_func():
                    settings.LOCKS.release(key)

                progress.except_func = except_func

                with transaction.atomic():
                    for operation_launch in operations_launch:

                        # Операции сумм разбивки по запускам/ заказам на продажу
                        operation_refs_sums = Operation_refs.objects.filter(
                            parent=operation_launch.operation,
                            child__opertype=settings.OPERS_TYPES_STACK.PRODUCTION_DETAIL_SUM_TASK
                        )
                        logger.debug(f'Операции сумм разбивки по запускам/ заказам на продажу: {operation_refs_sums.count()}')

                        for operation_refs_sum in operation_refs_sums:
                            operation_sum = operation_refs_sum.child

                            deleted = operation_refs_sum.delete()
                            logger.debug(f'deleted: {deleted}')

                            deleted = operation_sum.delete()
                            logger.debug(f'deleted: {deleted}')

                        # Техннологические операции
                        operation_refs_sums_dets = Operation_refs.objects.filter(
                            parent=operation_launch.operation,
                            child__opertype=settings.OPERS_TYPES_STACK.PRODUCTION_DETAIL_OPERS_TASK)

                        for operation_refs_sums_det in operation_refs_sums_dets:
                            logger.debug(f'Технологические операции: {operation_refs_sums_dets.count()}')

                            operations_operation = Operation_operation.objects.filter(operation=operation_refs_sums_det.child).order_by('-num')

                            for operation_operation in operations_operation:
                                # Выполнение по этим технологическим операциям
                                maked_values = Operation_refs.objects.filter(
                                    parent=operation_operation.operation,
                                    child__opertype=settings.OPERS_TYPES_STACK.MADE_OPERATIONS_PLS_TASK
                                ).order_by('-child_id')

                                maked_values = [o.child for o in maked_values]

                                logger.debug(f'Выполнение по ({operation_operation.num}) : {len(maked_values)}')
                                if len(maked_values) > 0:
                                    def func_refreshed(operation):
                                        Launches_viewManager.refreshRows(ids=parent_launch.id)
                                        Launches_viewManager.refreshRows(ids=child_launches)
                                        BuffersManager.fullRows()

                                    production_order_values_ext.delete_sums(operations=maked_values, func_refreshed=func_refreshed, parent=data)

                                deleted = Operation_refs.objects.filter(parent=operation_launch.operation, child=operation_operation.operation).delete()
                                logger.debug(f'deleted: {deleted}')

                                deleted = Operation_refs.objects.filter(parent__isnull=True, child=operation_operation.operation).delete()
                                logger.debug(f'deleted: {deleted}')

                                deleted = Operation_refs.objects.filter(parent__opertype__in=[settings.OPERS_TYPES_STACK.ROUTING_TASK], child=operation_operation.operation).delete()
                                logger.debug(f'deleted: {deleted}')

                                deleted = operation_operation.operation.delete()
                                logger.debug(f'deleted: {deleted}')

                            operation_det = operation_refs_sums_det.child
                            deleted = operation_refs_sums_det.delete()
                            logger.debug(f'deleted: {deleted}')

                            deleted = operation_det.delete()
                            logger.debug(f'deleted: {deleted}')

                        operation_executors = Operation_executor.objects.filter(operation=operation_launch.operation, props=Operation_executor.props.relevant)

                        for operation_executor in operation_executors:
                            operation_executor_stack.push(
                                item=Operation_executor_qty(executor=operation_executor.executor, qty=1),
                                logger=logger
                            )

                        deleted = Operation_refs.objects.filter(parent__isnull=True, child=operation_launch.operation).delete()
                        logger.debug(f'deleted: {deleted}')

                        deleted = Operation_refs.objects.filter(parent__opertype=settings.OPERS_TYPES_STACK.ROUTING_TASK, child=operation_launch.operation).delete()
                        logger.debug(f'deleted: {deleted}')

                        for operation_refs_launch in Operation_refs.objects.filter(parent=operation_launch.operation, child__opertype__in=[
                            settings.OPERS_TYPES_STACK.LAUNCH_TASK,
                        ]):
                            deleted = Operation_refs.objects.filter(parent__opertype=settings.OPERS_TYPES_STACK.PRODUCTION_TASK, child=operation_refs_launch.child).delete()
                            logger.debug(f'deleted: {deleted}')

                            _operation_refs_launch = operation_refs_launch.child

                            deleted = operation_refs_launch.delete()
                            logger.debug(f'deleted: {deleted}')

                            deleted = _operation_refs_launch.delete()
                            logger.debug(f'deleted: {deleted}')

                        deleted = operation_launch.operation.delete()

                        operation_launch_deleted += deleted[0]
                        logger.debug(f'deleted: {deleted}')

                        Launches_viewManager.refreshRows(ids=parent_launch.id)
                        if isinstance(child_launches, list) and len(child_launches) > 0:
                            ids = Production_orderManager.ids_list_2_int_list(child_launches)
                            Launches_viewManager.refreshRows(ids=ids)

                        if progress.step() != 0:
                            Launches_viewManager.fullRows()
                            settings.LOCKS.release(key)
                            raise ProgressDroped(progress_deleted)

                    for launch in Launches.objects.filter(parent=parent_launch):
                        # print(model_to_dict(launch))
                        launch.status = settings.PROD_OPERS_STACK.ROUTMADE
                        launch.save()

                        Launches_viewManager.refreshRows(ids=launch.id)

                    idx += 1
                    if idx == launch_cnt:
                        parent_launch.status = settings.PROD_OPERS_STACK.ROUTMADE
                        parent_launch.save()

                        Launches_viewManager.refreshRows(ids=parent_launch.id)
                        # progress.setContentsLabel('Обновление предстваления planing_production_order_mview')

                logger.debug(f'operation_executor_stack.len: {operation_executor_stack.len} сообщений')
                for operation_executor in operation_executor_stack:
                    settings.EVENT_STACK.EVENTS_PRODUCTION_ORDER_CREATE.send_message(
                        message=blinkString(f'<h4>Удалиено: {operation_executor.qty} заданий на производство.</h4>', bold=True),
                        users_array=[operation_executor.executor],
                        progress=progress,
                    )

            settings.LOCKS.release(key)
            return idx

        if operation_launch_deleted > 0:
            Production_orderManager.fullRows()
            BuffersManager.fullRows()

    def get_production_order_tmp_table(self, id, tmp_table_name=None):
        from isc_common.common.mat_views import create_tmp_table

        if tmp_table_name is None:
            tmp_table_name = f'''tmp_{uuid4()}'''

        create_tmp_table(
            on_commit=None,
            drop=False,
            sql_str='''SELECT distinct t.*
                                       FROM planing_operations po
                                                join planing_operation_item poi on po.id = poi.operation_id
                                                join planing_operation_item_add paoi on poi.item_id = paoi.item_id
                                                CROSS JOIN LATERAL
                                           json_to_recordset(paoi.item_full_name_obj::json) as t(
                                                                                                "confirmed" text,
                                                                                                "deliting" boolean,
                                                                                                "document__file_document" text,
                                                                                                "document_id" bigint,
                                                                                                "editing" boolean,
                                                                                                "id" bigint,
                                                                                                "isFolder" boolean,
                                                                                                "lastmodified" text,
                                                                                                "parent_id" bigint,
                                                                                                "props" bigint,
                                                                                                "qty_operations" int4,
                                                                                                "refs_id" bigint,
                                                                                                "refs_props" bigint,
                                                                                                "relevant" text,
                                                                                                "section" text,
                                                                                                "STMP_1_id" bigint,
                                                                                                "STMP_2_id" bigint,
                                                                                                "version" int4,
                                                                                                "where_from" text
                                           )
                                       where po.id = %s''',
            params=[id],
            table_name=tmp_table_name)
        return tmp_table_name

    def get_enabled_childs(self, id, launch, user, in_dict=True):
        from kaf_pas.planing.models.production_order_opers import Production_order_opers
        from kaf_pas.planing.models.production_order_opers_per_launch import Production_order_opers_per_launch

        if launch.parent is None:
            model_opers = Production_order_opers
        else:
            model_opers = Production_order_opers_per_launch

        def enable(operation):
            from kaf_pas.ckk.models.locations_users import Locations_users
            from kaf_pas.production.models.operation_executor import Operation_executor

            if user.is_develop or user.is_admin:
                return False
            else:
                users_ids = list(map(lambda x: x.user.id, Operation_executor.objects.filter(operation=operation.production_operation)))
                location_ids = list(map(lambda x: x.location.id, Locations_users.objects.filter(user_id=user)))

                if len(users_ids) > 0:
                    res = user.id in users_ids
                    return res
                else:
                    res = operation.resource.location.id in location_ids if operation.resource else False
                    return res

        def enable1(operation):
            res = ExecuteStoredProc('get_production_order_operation_ready', [operation.parent_id, user.id, operation.id])
            return res

        childs = list(model_opers.objects.filter(parent_id=id, launch=launch).order_by('production_operation_num'))
        childs = list(filter(lambda x: enable(x) is True, childs))

        _childs = []
        if len(childs) > 0:
            num = childs[0].production_operation_num
            for child in childs:
                if child.production_operation_num == num:
                    _childs.append(child)
                else:
                    break
                num += 1

        childs = _childs
        if in_dict is True:
            childs = list(map(lambda x: model_to_dict(x), childs))
        return childs

    def _create_tech_specification(self, data, old_data, key):
        from kaf_pas.production.models.operation_def_material import Operation_def_material
        from kaf_pas.production.models.operation_material import Operation_material
        from kaf_pas.production.models.operation_resources import Operation_resources
        from kaf_pas.production.models.operations_item import Operations_item

        created, updated, renumered, deleted = self.is_changed_data(data=data, old_data=old_data)
        logger.debug(f'is_changed_data: (created: {created}, updated: {updated}, renumered: {renumered}, deleted: {deleted})')

        if not created:
            return

        operations_item, created = Operations_item.objects.update_or_create(
            item=data.parentRecord.item,
            operation=data.production_operation,
            defaults=dict(
                description=data.description,
                ed_izm=data.production_operation_edizm,
                num=data.production_operation_num,
                props=Operations_item.props.created,
                qty=data.production_operation_qty,
            )
        )

        if not created:
            old_data = data
            operations_item.soft_restore()
            operations_item.props |= Operations_item.props.created
            operations_item.save()
            data.operation_item = operations_item
            logger.debug(f'\noperations_item: {operations_item}\n')

        operation_resources, created = Operation_resources.objects.update_or_create(
            operationitem=operations_item,
            defaults=dict(
                batch_size=1,
                location=data.location,
                location_fin=data.location_fin,
                resource=data.resource,
                resource_fin=data.resource_fin,
            )
        )
        if not created:
            operation_resources.soft_restore()
            logger.debug(f'\noperation_resources: {operation_resources}\n')

        for operation_def_material in Operation_def_material.objects.filter(operation_id=data.production_operation_id):
            operation_material, created = Operation_material.objects.update_or_create(
                operationitem=operations_item,
                defaults=dict(
                    material=operation_def_material.material,
                    material_askon=operation_def_material.material_askon,
                    edizm=operation_def_material.edizm,
                    qty=operation_def_material.qty)
            )

            if not created:
                operation_material.soft_restore()
                logger.debug(f'\noperation_material: {operation_material}\n')
        return old_data

    def insert_update_item(self, insert_item, bb, data):
        if len(bb) + 1 <= data.production_operation_num:
            bb.append(insert_item)
            insert_item.num = len(bb)
            insert_item.save()
        else:
            bb.insert(data.production_operation_num - 1, insert_item)
        return bb

    def _update_tech_specification(self, data, old_data, key):
        from kaf_pas.production.models.operation_resources import Operation_resources
        from kaf_pas.production.models.operations_item import Operations_item
        from kaf_pas.planing.models.operation_item import Operation_item
        from kaf_pas.planing.models.operation_operation import Operation_operation

        created, updated, renumered, deleted = self.is_changed_data(data=data, old_data=old_data)
        logger.debug(f'is_changed_data: (created: {created}, updated: {updated}, renumered: {renumered}, deleted: {deleted})')

        if not updated and not created and not deleted:
            return

        if deleted:
            data = old_data

        # Опреция задания на производство
        if data.parentRecord is not None:
            parent_operation_item = Operation_item.objects.get(operation=data.parentRecord.this)
        elif data.parent is not None:
            parent_operation_item = Operation_item.objects.get(operation=data.parent)
        else:
            raise Exception('Не найден parentRecord')

        if created:
            renumered = True
            aa = list(Operations_item.objects.filter(item=parent_operation_item.item, props=Operations_item.props.created).alive())
            if len(aa) > 1:
                raise Exception('Количество вставляемых операций может быть = 1')
            else:
                if len(aa) == 0:
                    aa = [data.operation_item]

                insert_item = aa[0]

                bb = list(Operations_item.objects.filter(item=parent_operation_item.item).alive().exclude(id__in=map(lambda x: x.id, aa)).order_by('num'))
                bb = self.insert_update_item(insert_item=insert_item, bb=bb, data=data)

        elif updated:
            if not renumered:
                renumered = flen(filter(lambda x: x.get('cnt') > 1, Operations_item.objects.filter(item=parent_operation_item.item).order_by('num').values('num').annotate(cnt=Count('num')))) > 0

            if renumered:
                aa = list(Operations_item.objects.filter(item=parent_operation_item.item, num=old_data.production_operation_num).alive())
                if len(aa) != 1:
                    raise Exception('Количество изменяемых операций может быть = 1')
                insert_item = aa[0]

                bb = list(Operations_item.objects.filter(item=parent_operation_item.item).alive().exclude(num=old_data.production_operation_num).order_by('num'))

                bb = self.insert_update_item(insert_item=insert_item, bb=bb, data=data)

            else:
                bb = Operations_item.objects.filter(item=parent_operation_item.item).alive().order_by('num')
        elif deleted:
            renumered = True
            operations = map(lambda x: x.operation, Operation_item.objects.filter(item=parent_operation_item.item, operation__deleted_at__isnull=False))
            prod_operations = map(lambda x: x.production_operation, Operation_operation.objects.filter(operation__in=operations))
            deleting_operations = Operations_item.objects.filter(item=parent_operation_item.item, operation__in=prod_operations)
            for deleting_operation in deleting_operations:
                deleted = deleting_operation.soft_delete()
                logger.debug(f'\ndeleted: {deleted}\n')

            bb = Operations_item.objects.filter(item=parent_operation_item.item).alive().order_by('num')
        else:
            raise Exception('Unknown type')

        if renumered:
            num = 1
            for updatedItem in bb:
                if updatedItem.num != num:
                    updatedItem.old_num = updatedItem.num
                    updatedItem.num = num
                    updatedItem.save()
                num += 1

        if updated:
            operations_item = bb[data.production_operation_num - 1]
            operations_item.qty = data.production_operation_qty
            operations_item.color = data.production_operation_color
            operations_item.ed_izm = data.production_operation_edizm
            operations_item.description = data.description
            operations_item.save()

            for operation_resources in Operation_resources.objects.filter(operationitem=operations_item):
                # Данные по ресурсам и местоположениям данной операции
                operation_resources.location = data.location
                operation_resources.resource = data.resource
                operation_resources.resource_fin = data.resource_fin
                operation_resources.location_fin = data.location_fin
                operation_resources.save()
        pass

    def _update_prod_specifications_mat_res(self, launch_operations_item, operation_item, key):
        from kaf_pas.production.models.operation_resources import Operation_resources
        from kaf_pas.production.models.launch_operation_resources import Launch_operation_resources
        from kaf_pas.production.models.launch_operation_material import Launch_operations_material
        from kaf_pas.production.models.operation_material import Operation_material
        # Изменяем ресурсы согласно технологической спецификации
        for operation_resource in Operation_resources.objects.filter(operationitem=operation_item):

            for launch_operation_resources in Launch_operation_resources.objects.filter(operation_resources=operation_resource, launch_operationitem=launch_operations_item):
                if operation_resource.resource is not None:
                    launch_operation_resources.resource = operation_resource.resource

                if operation_resource.resource_fin is not None:
                    launch_operation_resources.resource_fin = operation_resource.resource_fin

                launch_operation_resources.location = operation_resource.location
                launch_operation_resources.location_fin = operation_resource.location_fin
                launch_operation_resources.batch_size = operation_resource.batch_size
                launch_operation_resources.save()

        # Изменяем материалы согласно технологической спецификации
        for operation_material in Operation_material.objects.filter(operationitem=operation_item):
            for launch_operation_material in Launch_operations_material.objects.filter(operation_material=operation_material, launch_operationitem=launch_operations_item):
                launch_operation_material.edizm = operation_material.edizm
                launch_operation_material.material = operation_material.material
                launch_operation_material.material_askon = operation_material.material_askon
                launch_operation_material.qty = operation_material.qty
                launch_operation_material.save()

    def _update_prod_specifications(self, data, old_data, user, key):
        from django.conf import settings
        from kaf_pas.planing.models.operation_launch_item import Operation_launch_item
        from kaf_pas.planing.models.operation_operation import Operation_operation
        from kaf_pas.production.models.launch_operation_material import Launch_operations_material
        from kaf_pas.production.models.launch_operation_resources import Launch_operation_resources
        from kaf_pas.production.models.launch_operations_item import Launch_operations_item
        from kaf_pas.production.models.operation_material import Operation_material
        from kaf_pas.production.models.operations_item import Operations_item
        from kaf_pas.production.models.operation_resources import Operation_resources
        from kaf_pas.production.models.launches import Launches

        created, updated, renumered, deleted = self.is_changed_data(data=data, old_data=old_data)
        logger.debug(f'is_changed_data: (created: {created}, updated: {updated}, renumered: {renumered}, deleted: {deleted})')

        if not updated and not created and not deleted:
            return

        if deleted:
            data = old_data

        if data.parentRecord is not None:
            parentRecord = data.parentRecord
        elif data.parent is not None:
            parentRecord = data.parent
        else:
            raise Exception('Не найден parentRecord')

        if parentRecord.launch.parent is not None:
            launches = [parentRecord.launch]
        else:
            launches = parentRecord.launch.child_launches

        launch_operations_items_stack = Stack()

        if deleted:
            # Удаляем операции не входящие в технологическую спецификацию
            for launch_operations_item in Launch_operations_item.objects. \
                    filter(launch__in=launches). \
                    filter(operationitem_id__in=list(map(lambda x: x.id, Operations_item.objects.filter(item=parentRecord.item, deleted_at__isnull=False)))). \
                    alive(). \
                    exclude(launch__status=settings.PROD_OPERS_STACK.CLOSED):

                launch_operation_resources = Launch_operation_resources.objects.filter(launch_operationitem=launch_operations_item).soft_delete()
                if launch_operation_resources is not None:
                    logger.debug(f'\nLaunch_operation_resources deleted: {launch_operation_resources}\n')

                launch_operations_material = Launch_operations_material.objects.filter(launch_operationitem=launch_operations_item).soft_delete()
                if launch_operations_material is not None:
                    logger.debug(f'\nLaunch_operations_material deleted: {launch_operations_material}\n')

                launch_operations_item_deleted = launch_operations_item.soft_delete()
                if launch_operations_item_deleted is not None:
                    launch_operations_items_stack.push(launch_operations_item)
                    logger.debug(f'\nlaunch_operations_item deleted: {launch_operations_item_deleted}\n')

        # Изменяем операции согласно изменений технологической спецификации
        if updated:
            for operation_item in Operations_item.objects.filter(item=parentRecord.item).order_by('num'):
                for launch in launches:
                    for launch_operations_item in Launch_operations_item.objects.filter(item=operation_item.item, launch=launch, operation=operation_item.operation):

                        if launch_operations_item.operationitem == operation_item:
                            pass

                        if launch_operations_item.launch.status == settings.PROD_OPERS_STACK.CLOSED:
                            continue

                        # launch_operations_item.description = 'Обновлено'
                        launch_operations_item.ed_izm = operation_item.ed_izm
                        launch_operations_item.color = operation_item.color
                        launch_operations_item.num = operation_item.num
                        launch_operations_item.old_num = operation_item.old_num
                        launch_operations_item.qty = operation_item.qty
                        launch_operations_item.props = Launch_operations_item.props.updated
                        launch_operations_item.deleted_at = operation_item.deleted_at
                        launch_operations_item.save()

                        launch_operations_items_stack.push(launch_operations_item)
                        logger.debug(f'\nlaunch_operations_item: {launch_operations_item}\n')

                        # Изменяем ресурсы согласно технологической спецификации
                        self._update_prod_specifications_mat_res(
                            launch_operations_item=launch_operations_item,
                            operation_item=operation_item,
                            key=key
                        )

        elif deleted:
            for operation_item in Operations_item.objects.filter(item=parentRecord.item, deleted_at__isnull=False):
                # for launch_operations_item in Launch_operations_item.objects.filter(item=operation_item.item, launch__in=launches):
                #     launch_operations_item.soft_delete()

                for _launch_operations_item in Launch_operations_item.objects.filter(item=operation_item.item, launch__in=launches).alive():
                    for _operations_item in Operations_item.objects.filter(item=operation_item.item, operation=_launch_operations_item.operation):
                        if _launch_operations_item.num != _operations_item.num:
                            _launch_operations_item.num = _operations_item.num
                            _launch_operations_item.save()

        elif created:
            created_operation_items = Operations_item.objects.filter(item=parentRecord.item, props=Operations_item.props.created).order_by('num')
            for operation_item in created_operation_items:
                launches = Launch_operations_item.objects.filter(item=operation_item.item, launch__in=launches).values('launch').distinct()
                for launch_dict in launches:
                    launch_operations_item, created = Launch_operations_item.objects.update_or_create(
                        item=operation_item.item,
                        launch=Launches.objects.get(id=launch_dict.get('launch')),
                        operation=operation_item.operation,
                        operationitem=operation_item,
                        color=operation_item.color,
                        defaults=dict(
                            description=data.description,
                            ed_izm=operation_item.ed_izm,
                            num=operation_item.num,
                            old_num=operation_item.old_num,
                            props=operation_item.props.created,
                            qty=operation_item.qty,
                        )
                    )

                    if not created:
                        if launch_operations_item.is_deleted:
                            launch_operations_item.soft_restore()
                            launch_operations_items_stack.push(launch_operations_item)
                            created = True
                    else:
                        launch_operations_items_stack.push(launch_operations_item)

                    if created:
                        try:
                            operation_resources = Operation_resources.objects.get(operationitem=operation_item)

                            launch_operation_resources, created = Launch_operation_resources.objects.update_or_create(
                                launch_operationitem=launch_operations_item,
                                defaults=dict(
                                    batch_size=operation_resources.batch_size,
                                    location=operation_resources.location,
                                    location_fin=operation_resources.location_fin,
                                    operation_resources=operation_resources,
                                    resource=operation_resources.resource if operation_resources.resource else operation_resources.location.resource,
                                    resource_fin=operation_resources.resource_fin,
                                )
                            )
                            logger.debug(f'\nlaunch_operation_resources.resource: {launch_operation_resources}\n')

                            if not created:
                                launch_operation_resources.soft_restore()

                            launch_operations_item.resource = launch_operation_resources.resource
                            launch_operations_item.resource_fin = launch_operation_resources.resource_fin
                            launch_operations_item.location_fin = launch_operation_resources.location_fin
                        except Operation_resources.DoesNotExist:
                            raise Exception('Resource not found')

                        logger.debug(f'\nlaunch_operations_item.resource: {launch_operations_item.resource}\n')
                        logger.debug(f'\nlaunch_operations_item.location_fin: {launch_operations_item.location_fin}\n')

                        launch_operations_item.operation_materials = Stack()
                        for operation_material in Operation_material.objects.filter(operationitem=operation_item):
                            launch_operations_material, created = Launch_operations_material.objects.update_or_create(
                                launch_operationitem=launch_operations_item,
                                defaults=dict(
                                    edizm=operation_material.edizm,
                                    material=operation_material.material,
                                    material_askon=operation_material.material_askon,
                                    operation_material=operation_material,
                                    qty=operation_material.qty
                                )
                            )

                            if not launch_operations_material:
                                launch_operations_material.soft_restore()

                            logger.debug(f'\nlaunch_operations_material: {launch_operations_material}\n')
                            launch_operations_item.operation_materials.push(operation_material)

                        logger.debug(f'\nlaunch_operations_item.operation_materials: {launch_operations_item.operation_materials}\n')

                        try:
                            operation_launch_item = Operation_launch_item.objects.get(
                                launch_item=launch_operations_item,
                                operation__opertype=settings.OPERS_TYPES_STACK.ROUTING_TASK
                            )
                            logger.debug(f'\noperation_launch_item: {operation_launch_item}\n')

                        except Operation_launch_item.DoesNotExist:
                            operation = self.rec_operation(
                                description=data.description,
                                item=parentRecord.item,
                                launch=parentRecord.launch,
                                operation=parentRecord.this,
                                operation_item=launch_operations_item,
                                opertype=settings.OPERS_TYPES_STACK.ROUTING_TASK,
                                props=Operation_operation.props.direct_created,
                                status=settings.OPERS_TYPES_STACK.ROUTING_TASK_STATUSES.get(new),
                                user=user,
                            )
                            logger.debug(f'\noperation: {operation}\n')

                            operation_launch_item = Operation_launch_item.objects.create(
                                operation=operation,
                                launch_item=launch_operations_item
                            )
                            logger.debug(f'\noperation_launch_item: {operation_launch_item}\n')

                for _launch_operations_item in Launch_operations_item.objects.filter(item=operation_item.item, launch__in=launches).alive().order_by('num', '-lastmodified'):
                    _operations_item = Operations_item.objects.get(id=_launch_operations_item.operationitem.id)
                    if _launch_operations_item.num != _operations_item.num:
                        _launch_operations_item.num = _operations_item.num
                        _launch_operations_item.save()

                operation_item.props &= ~ Operations_item.props.created
                operation_item.save()

        return launch_operations_items_stack

    def _update_routing(self, data, old_data, updated_launch_operations_items: Stack, user, key):

        created, updated, renumered, deleted = self.is_changed_data(data=data, old_data=old_data)
        logger.debug(f'is_changed_data: (created: {created}, updated: {updated}, renumered: {renumered}, deleted: {deleted})')

        if not renumered and not created and not deleted:
            return

        if deleted:
            data = old_data

        self.routing_ext.update_routing(data=data, old_data=old_data, updated_launch_operations_items=updated_launch_operations_items, user=user, key=key)

    def _created_production_orders(self, data, old_data, user, updated_launch_operations_items, key):
        from django.conf import settings
        from kaf_pas.planing.models.operation_launch_item import Operation_launch_item
        from kaf_pas.planing.models.operation_operation import Operation_operation
        from kaf_pas.planing.models.operation_refs import Operation_refs
        from kaf_pas.planing.models.production_order_opers import Production_order_opers
        from kaf_pas.planing.models.production_order_values_ext import Production_orderWrapper
        from kaf_pas.production.models.launch_operation_material import Launch_operations_material
        from kaf_pas.production.models.launch_operation_resources import Launch_operation_resources
        from kaf_pas.production.models.launch_operations_item import Launch_operations_item

        if old_data is not None:
            parent = data.parent
            if parent is None:
                parent = data.parentRecord.this

            operations = list(map(lambda x: x.child, Operation_refs.objects.filter(parent=parent, child__opertype__code=DETAIL_OPERS_PRD_TSK)))
            if len(operations) == 0:
                old_data = None

        created, updated, renumered, deleted = self.is_changed_data(data=data, old_data=old_data)

        if not created:
            return

        logger.debug(f'is_changed_data: (created: {created}, updated: {updated}, renumered: {renumered}, deleted: {deleted})')

        opers_stack = Set()
        for created_launch_operations_item in updated_launch_operations_items:
            _continue = False

            for if_deleted_operation in data.parentRecord.all_childs.filter(production_operation=created_launch_operations_item.operation):
                if if_deleted_operation.is_deleted:
                    for operation_refs in Operation_refs.objects.filter(child_id=if_deleted_operation.id, parent_id=if_deleted_operation.parent_id):
                        for operation_operation in Operation_operation.objects.filter(operation=operation_refs.child):
                            deleted = operation_operation.operation.soft_restore()
                            _continue = deleted is not None

            if _continue:
                continue

            if opers_stack.is_exists(created_launch_operations_item.operation.id):
                continue

            operation_launch_item = list(map(lambda x: x.launch_item, Operation_launch_item.objects.filter(
                launch_item=created_launch_operations_item,
                # operation__opertype__code__in=[DETAIL_OPERS_PRD_TSK]
            ).distinct()))
            logger.debug(f'\noperation_launch_item: {operation_launch_item}')

            operation_resources = Launch_operation_resources.objects.filter(launch_operationitem__in=operation_launch_item)
            operation_materials = list(Launch_operations_material.objects.filter(launch_operationitem__in=operation_launch_item))

            if operation_resources.count() == 0:
                raise Exception('Not found resource')
            if operation_resources.count() > 1:
                raise Exception('Resources must be == 1')
            operation_resources = operation_resources[0]
            logger.debug(f'\noperation_resources: {operation_resources}')

            operationitem = Production_orderWrapper(
                color=created_launch_operations_item.color,
                ed_izm=created_launch_operations_item.ed_izm,
                location_fin=operation_resources.location_fin,
                num=created_launch_operations_item.num,
                operation=created_launch_operations_item.operation,
                operation_materials=operation_materials,
                qty=created_launch_operations_item.qty,
                resource=operation_resources.resource,
                resource_fin=operation_resources.resource_fin,
            )

            if data.parentRecord.launch.parent is None:
                launch = data.parentRecord.launch
            else:
                launch = data.parentRecord.launch.parent

            operation_det = self.rec_operation(
                description=data.description,
                item=data.parentRecord.item,
                launch=launch,
                operation=data.parentRecord.this,
                operation_item=operationitem,
                opertype=settings.OPERS_TYPES_STACK.PRODUCTION_DETAIL_OPERS_TASK,
                props=Operation_operation.props.direct_created,
                status=settings.OPERS_TYPES_STACK.PRODUCTION_DETAIL_OPERS_TASK_STATUSES.get(new),
                user=user,
            )

            # Проверить наличие операций у соседей
            production_order_opers = Production_order_opers.objects.get(id=operation_det.id)
            if production_order_opers.right_neighbour is not None and production_order_opers.right_neighbour.has_moving_operations:
                raise Exception(f'Операцию вставить или нельзя, у следующей операции уже было движение позиций.')

            operations = list(map(lambda x: x.child, Operation_refs.objects.filter(parent=data.parentRecord.this, child__opertype__code=DETAIL_OPERS_PRD_TSK)))
            operations_operation = list(Operation_operation.objects.filter(operation__in=operations).order_by('num'))

            if data.parentRecord.launch.parent is not None:
                launches = [data.parentRecord.launch]
            else:
                launches = data.parentRecord.launch.child_launches

            launch_operations_items = None
            for launch in launches:
                launch_operations_items = Launch_operations_item.objects.filter(launch=launch, item=data.parentRecord.item).alive().order_by('num')
                if len(launch_operations_items) == len(operations):
                    break

            if launch_operations_items is None:
                raise Exception(f'Production spec not found')

            for operation_operation in operations_operation:
                for production_operation in filter(lambda x: x.operation.id == operation_operation.production_operation.id, launch_operations_items):
                    if production_operation.num != operation_operation.num:
                        operation_operation.num = production_operation.num
                        operation_operation.save()

        return old_data

    def _update_production_orders(self, data, old_data, user, updated_launch_operations_items, key):
        from kaf_pas.planing.models.operation_operation import Operation_operation
        from kaf_pas.planing.models.operation_refs import Operation_refs
        from kaf_pas.planing.models.operation_resources import Operation_resources
        from kaf_pas.production.models.launch_operation_resources import Launch_operation_resources
        from kaf_pas.planing.operation_typesStack import DETAIL_OPERS_PRD_TSK
        from kaf_pas.production.models.launch_operations_item import Launch_operations_item

        created, updated, renumered, deleted = self.is_changed_data(data=data, old_data=old_data)
        logger.debug(f'is_changed_data: (created: {created}, updated: {updated}, renumered: {renumered}, deleted: {deleted})')

        if not updated and not deleted:
            return

        if deleted:
            data = old_data

        operations = list(map(lambda x: x.child, Operation_refs.objects.filter(parent=data.parent, child__opertype__code=DETAIL_OPERS_PRD_TSK)))
        operations_operation = Operation_operation.objects.filter(operation__in=operations).order_by('num')

        for updated_launch_operations_item in updated_launch_operations_items:
            try:
                if updated:
                    for operation_operation in operations_operation.filter(production_operation=updated_launch_operations_item.operation):
                        logger.debug(f'operation_operation: {operation_operation}')
                        operation_operation.soft_restore()

                        operation_resources = Operation_resources.objects.get(operation=operation_operation.operation, deleted_at=None)
                        logger.debug(f'\n------operation_resources: {operation_resources}')
                        launch_operation_resources = Launch_operation_resources.objects.get(launch_operationitem=updated_launch_operations_item)
                        logger.debug(f'\n------launch_operation_resources: {launch_operation_resources}')

                        operation_resources.location_fin = launch_operation_resources.location_fin
                        operation_resources.resource = launch_operation_resources.resource
                        operation_resources.resource_fin = launch_operation_resources.resource_fin
                        operation_resources.save()
                        logger.debug(f'operation_resources: {operation_resources}')

                        operation_operation.production_operation = updated_launch_operations_item.operation
                        operation_operation.ed_izm = updated_launch_operations_item.ed_izm
                        operation_operation.color = updated_launch_operations_item.color

                        if operation_operation.num != updated_launch_operations_item.num:
                            operation_operation.num = updated_launch_operations_item.num
                            operation_operation.old_num = updated_launch_operations_item.old_num
                            # self._re_arrange_neighbour()

                        operation_operation.color = updated_launch_operations_item.color
                        operation_operation.qty = updated_launch_operations_item.qty
                        operation_operation.deleted_at = updated_launch_operations_item.deleted_at
                        operation_operation.save()

                elif deleted:
                    if updated_launch_operations_item.is_deleted:
                        for operation_operation in Operation_operation.objects.filter(
                                operation__in=operations,
                                production_operation=updated_launch_operations_item.operation
                        ):
                            # self._re_arrange_neighbour()
                            operation_operation.soft_delete()
            except Operation_operation.DoesNotExist:
                pass

        if deleted:
            for operation_operation in Operation_operation.objects.filter(operation__in=operations).alive().order_by('num'):
                for launch_operations_item in Launch_operations_item.objects.filter(
                        item=data.parent.item,
                        launch=data.launch if data.launch.parent is not None else data.launch.child_launches[0],
                        operation=operation_operation.production_operation,
                ).alive():
                    if operation_operation.num != launch_operations_item.num:
                        operation_operation.num = launch_operations_item.num
                        operation_operation.save()

    def is_changed_data(self, data, old_data):
        if data is None:
            return False, False, False, True

        if old_data is None:
            return True, False, False, False

        if data.resource != old_data.resource:
            data.resource.location = old_data.resource.location
            return False, True, False, False

        if data.resource_fin != old_data.resource_fin:
            data.resource_fin.location = old_data.resource_fin.location
            return False, True, False, False

        if data.location != old_data.location:
            data.resource = data.location.resource
            return False, True, False, False

        if data.location_fin != old_data.location_fin:
            data.resource_fin = data.location_fin.resource
            return False, True, False, False

        if data.production_operation_num != old_data.production_operation_num:
            # if data.this.opertype == settings.OPERS_TYPES_STACK.PRODUCTION_TASK:
            #     if flen(data.this.minus_values) > 0:
            #         raise Exception(f'Выполнение невозможно, есть связанные выпуски.')
            return False, True, True, False

        if data.production_operation_qty != old_data.production_operation_qty:
            return False, True, False, False

        if data.production_operation_edizm_id != old_data.production_operation_edizm_id:
            return False, True, False, False

        if data.production_operation_id != old_data.production_operation_id:
            return False, True, False, False

        if data.description != old_data.description:
            return False, True, False, False

        if data.color != old_data.color:
            return False, True, False, False

        if data.production_operation_color_id != old_data.production_operation_color_id:
            return False, True, False, False

        return False, True, False, False

    def _refreshed_operations_view(self, data, old_data, user):
        from kaf_pas.planing.models.production_order_opers import Production_order_opersManager
        from kaf_pas.planing.models.production_order import Production_orderManager

        created, updated, renumered, deleted = self.is_changed_data(data=data, old_data=old_data)
        logger.debug(f'is_changed_data: (created: {created}, updated: {updated}, renumered: {renumered}, deleted: {deleted})')
        if not created and not updated and not renumered and not deleted:
            return

        if deleted:
            parent_id = old_data.parent.id
        elif created:
            parent_id = data.parentRecord.this.id
        elif updated:
            parent_id = data.parent.id
        else:
            raise Exception('parent Not Found')

        Production_orderManager.update_redundant_planing_production_order_table(ids=parent_id, user=user)

        if updated and old_data is not None and not renumered:
            # Production_order_opersManager.refreshRows(ids=data.id, user=user)
            Production_order_opersManager.fullRows(suffix=f'''_{parent_id}''')
        elif created or renumered or deleted:
            Production_order_opersManager.fullRows(suffix=f'''_{parent_id}''')

        Production_orderManager.refreshRows(parent_id, user=user)

    def _delete_tech_specification(self, id, key, user):
        from kaf_pas.planing.models.operations import Operations
        from kaf_pas.planing.models.production_order_opers import Production_order_opers
        from kaf_pas.planing.models.production_order_opers import Production_order_opersManager
        from kaf_pas.planing.models.production_order_values_ext import Production_orderWrapper

        production_order_opers = Production_order_opers.objects.get(id=id)
        if production_order_opers.has_moving_operations:
            raise Exception(f'Операцию удалить нельзя, уже было движение позиций.')

        operation = Operations.objects.get(id=production_order_opers.id)
        operation.soft_delete()

        data = None

        old_data = Production_order_opersManager.getRecord(record=Production_order_opers.objects.get(id=id), user=user)
        logger.debug(f'old_data: {old_data}')

        old_data = Production_orderWrapper(**old_data)

        # Меняем порядок строк операций в технологической спецификации с учетом удаленной
        self._update_tech_specification(data=data, old_data=old_data, key=key)

        # Меняем порядок строк операций вв производственных спецификациях с учетом удаленной
        updated_launch_operations_items = self._update_prod_specifications(data=data, old_data=old_data, user=user, key=key)

        # Корректируем маршрутизацию согласно порядку следования операций
        # self._update_routing(data=data, old_data=old_data, updated_launch_operations_items=updated_launch_operations_items, user=user, key=key)

        # Коректируем делаизацию заказа на производсво, в плане операций
        self._update_production_orders(updated_launch_operations_items=updated_launch_operations_items, data=data, old_data=old_data, user=user, key=key)

        # Обновляем грид операций
        self._refreshed_operations_view(data=data, old_data=old_data, user=user)

    def update_operation(self, data, user, old_data=None):
        from django.conf import settings
        from django.db import transaction
        from kaf_pas.planing.models.production_order_opers import Production_order_opers
        from kaf_pas.planing.models.production_order_opers import Production_order_opersManager
        from kaf_pas.production.models.operation_def_resources import Operation_def_resources
        from kaf_pas.planing.models.production_order_values_ext import Production_orderWrapper

        logger.debug(f'data={data}')
        logger.debug(f'old_data={old_data}')

        if data is not None:
            if data.get('location_id') is None and data.get('resource_id') is None:
                try:
                    operation_def_resources = Operation_def_resources.objects.get(operation_id=data.get('production_operation_id'))
                    setAttr(data, 'location_id', operation_def_resources.location.id if operation_def_resources.location else None)
                    setAttr(data, 'location_fin_id', operation_def_resources.location_fin.id if operation_def_resources.location_fin else None)
                    setAttr(data, 'resource_id', operation_def_resources.resource.id if operation_def_resources.resource else None)
                    setAttr(data, 'resource_fin_id', operation_def_resources.resource_fin.id if operation_def_resources.resource_fin else None)

                except Operation_def_resources.DoesNotExist:
                    raise Exception('Не определен ресурс или местоположение.')

        with transaction.atomic():
            key = f'''update_operation_{data.get('id')}''' if data.get('id') is not None else None
            try:
                if key is not None:
                    settings.LOCKS.acquire(key)

                    if data.get('id') is not None:
                        try:
                            production_order_opers = Production_order_opers.objects.get(id=data.get('id'))
                            if data is not None and old_data is not None:
                                if data.get('production_operation_num') != old_data.get('production_operation_num'):
                                    if production_order_opers.has_moving_operations:
                                        raise Exception(f'Операцию переместить нельзя нельзя, уже было движение позиций.')

                            check_data = Production_order_opersManager.getRecord(record=production_order_opers, user=user)

                            delAttr(old_data, 'date')
                            delAttr(old_data, 'value_made')
                            delAttr(old_data, 'value_start')
                            delAttr(old_data, 'value_odd')
                            delAttr(old_data, 'value_odd_ship')
                            delAttr(old_data, 'edizm__name')
                            delAttr(old_data, 'launch_id')

                            delAttr(check_data, 'date')
                            delAttr(check_data, 'value_made')
                            delAttr(check_data, 'value_odd')
                            delAttr(check_data, 'value_odd_ship')
                            delAttr(check_data, 'value_start')
                            delAttr(check_data, 'edizm__name')
                            delAttr(check_data, 'launch_id')

                            messages = compare_2_dict(old_data, check_data)
                            if len(messages) > 0:
                                Production_order_opersManager.refreshRows(ids=check_data.get('id'), user=user)
                                settings.LOCKS.release(key)
                                messages_str = '\n'.join(messages)
                                raise Exception(f'''<pre>'Данные операции изменились, повторите выполнение, \n'{messages_str}</pre>''')
                        except Production_order_opers.DoesNotExist:
                            Production_order_opersManager.fullRows()
                            settings.LOCKS.release(key)
                            raise Exception('''Операция уже удалена''')

                data = Production_orderWrapper(**data)
                old_data = Production_orderWrapper(**old_data) if old_data is not None else None

                # Cоздаем новую операцию
                old_data = self._create_tech_specification(data=data, old_data=old_data, key=key)

                # Меняем строку операции в технологической спецификации
                self._update_tech_specification(data=data, old_data=old_data, key=key)

                # Меняем строки операций в производственных спецификациях, которые относятся к запуску из data получаем список измененных строк
                updated_launch_operations_items = self._update_prod_specifications(data=data, user=user, old_data=old_data, key=key)

                # Корректируем маршрутизацию согласно порядку следования операций
                # self._update_routing(data=data, old_data=old_data, updated_launch_operations_items=updated_launch_operations_items, user=user, key=key)

                # Создаем новую операцию в детаизации заказа на производсво, в плане операций
                old_data = self._created_production_orders(updated_launch_operations_items=updated_launch_operations_items, data=data, old_data=old_data, user=user, key=key)

                # Коректируем делаизацию заказа на производсво, в плане операций
                self._update_production_orders(updated_launch_operations_items=updated_launch_operations_items, data=data, old_data=old_data, user=user, key=key)

                # Обновляем грид операций
                self._refreshed_operations_view(data=data, old_data=old_data, user=user)

                if key is not None:
                    settings.LOCKS.release(key)
            except Exception as ex:
                if key is not None:
                    settings.LOCKS.release(key)
                raise ex

            # raise NotImplement()
        return data

    def delete_operation(self, ids, user):
        from django.conf import settings
        from django.db import transaction
        from kaf_pas.planing.models.operation_refs import Operation_refs
        from kaf_pas.planing.operation_typesStack import DETAIL_OPERS_PRD_TSK

        if isinstance(ids, int):
            ids = [ids]

        with transaction.atomic():
            childs = Operation_refs.objects.filter(
                parent__in=map(lambda x: x.parent, Operation_refs.objects.filter(child_id__in=ids)),
                child__opertype__code__in=[DETAIL_OPERS_PRD_TSK],
                child__deleted_at=None
            )

            if childs.count() == len(ids):
                raise Exception('Удалить все операции нельзя.')

            for id in ids:
                logger.debug(f'id: {id}')
                key = f'''delete_operation_{id}'''
                settings.LOCKS.acquire(key)

                try:
                    self._delete_tech_specification(id=id, key=key, user=user)

                    settings.LOCKS.release(key)
                except Exception as ex:
                    settings.LOCKS.release(key)
                    raise ex

            # raise NotImplement()

    def get_exists_in_production_query(self, item=None):
        from isc_common.common.functions import delete_dbl_spaces
        from kaf_pas.planing.models.production_order import Production_order

        STMP_2 = item.STMP_2.value_str if item.STMP_2 else None
        STMP_1 = item.STMP_1.value_str if item.STMP_1 else None

        if STMP_2 is None:
            query = Production_order.objects.filter(item__STMP_1__value_str__delete_dbl_spaces=delete_dbl_spaces(STMP_1))
        elif STMP_1 is None:
            query = Production_order.objects.filter(item__STMP_2__value_str__delete_dbl_spaces=delete_dbl_spaces(STMP_2))
        else:
            query = Production_order.objects.filter(item__STMP_1__value_str__delete_dbl_spaces=delete_dbl_spaces(STMP_1),
                                                    item__STMP_2__value_str__delete_dbl_spaces=delete_dbl_spaces(STMP_2))
        return query.exclude(status__code=closed).exclude(status__code=doing).exclude(value_odd=0).filter(id=F('id_f'))

    def check_exists_in_production(self, qty, user, item=None, demand=None, launch__date=None, callbackData=None):
        from kaf_pas.ckk.models.locations import Locations

        query = self.get_exists_in_production_query(item=item)

        value = 0
        messeges = []
        for production_order in query:
            ed_izm_str = ",".join(production_order.edizm_arr) if production_order.edizm_arr is not None else ''
            messeges.append(f'{production_order.launch.code} от {DateToStr(production_order.launch.date)} на: {Locations.objects.get(id=production_order.location_ids[0]).full_name} в количестве {DecimalToStr(production_order.value_odd)} {ed_izm_str}')
            value += production_order.value_odd

        text = '\n'.join(messeges)

        if value > 0:
            if callbackData is not None and (
                    value == ToDecimal(callbackData.get('value')) and
                    qty == ToDecimal(callbackData.get('qty')) and
                    ed_izm_str == callbackData.get('ed_izm_str', '') and
                    production_order.item.id == callbackData.get('item_id') and
                    production_order.launch.id == callbackData.get('launch_id')):
                return None

            if callbackData is None:
                message_str = blinkString(
                    text=f'''<pre>{production_order.item.item_name} (ID={production_order.item.id}) присутствует в запуске(ах):\n{text}, \nЗапустить дополнительно?</pre>''',
                    blink=False,
                    color=blue, bold=True)

                WebSocket.send_ask_message(
                    host=settings.WS_HOST,
                    port=settings.WS_PORT,
                    channel=f'common_{user.username}',
                    message=message_str,
                    callbackData=dict(
                        demand_id=demand.id if demand is not None else None,
                        ed_izm=ed_izm_str,
                        item_id=production_order.item.id,
                        launch__date=launch__date,
                        launch_id=production_order.launch.id,
                        qty=qty,
                        user_id=user.id,
                        value=value,
                    ),
                    logger=logger
                )
                return production_order
            else:
                return None
        return None

    def make_production_order_by_hand(self, data, user):
        from django.db import transaction
        from kaf_pas.production.models.launches import Launches
        from kaf_pas.planing.models.production_order_values_ext import Production_orderWrapper
        from kaf_pas.sales.models.demand import Demand

        with transaction.atomic():
            logger.debug(f'data={data}')

            callbackData = data.get('callbackData')
            item_id = data.get('item_id')

            demand = None

            qty = data.get('qty')
            launch__date = data.get('launch__date')

            if callbackData is not None and item_id is None:
                setAttr(data, 'item_id', callbackData.get('item_id'))
                setAttr(data, 'demand_id', callbackData.get('demand_id'))

            demand_id = data.get('demand_id')
            if demand_id is not None:
                demand = Demand.objects.get(id=demand_id)

            if callbackData is not None and qty is None:
                setAttr(data, 'qty', callbackData.get('qty'))

            if callbackData is not None and launch__date is None:
                setAttr(data, 'launch__date', callbackData.get('launch__date'))

            data = Production_orderWrapper(**data)

            parentlaunch, create = Launches.objects.get_or_create(
                code='000',
                defaults=dict(
                    date=datetime.now(),
                    status=settings.PROD_OPERS_STACK.HANDMADE
                )
            )

            if self.check_exists_in_production(
                    item=data.item,
                    demand=data.demand,
                    qty=data.qty,
                    user=user,
                    launch__date=launch__date,
                    callbackData=callbackData) is not None:
                return

            key = f'LaunchesManager.make_production_order_by_hand{data.item_id}'
            settings.LOCKS.acquire(key)

            try:
                launches_ext = Launches_ext()
                date = StrToDate(data.launch__date)

                # Составляем производственную спецификацию
                _, launch = launches_ext.rec_launch(
                    date=date,
                    description=data.description,
                    item=data.item,
                    key=key,
                    mode='update',
                    parentlaunch=parentlaunch,
                    qty=data.qty,
                    user=user,
                    demand=demand
                )
                logger.debug(f'launch: {launch}')

                settings.LOCKS.release(key)
                # raise NotImplement()
            except Exception as ex:
                settings.LOCKS.release(key)
                raise ex

    def get_use_4_grouping_message(self, location_id):
        from kaf_pas.ckk.models.locations_users import Locations_users
        from isc_common.auth.models.user import User

        users = list(map(lambda x: x.user, Locations_users.objects.filter(location_id=location_id)))
        users1 = list(User.objects.filter(usergroup__code='administrators'))
        users.extend(users1)
        users = list(set(users))
        return users

    def get_main_launches(self, records):
        from kaf_pas.production.models.launches import Launches

        launch_ids_set = set(list(map(lambda x: x.get('launch_id'), records)))
        launch_child_ids_set = set(list(map(lambda x: x.parent.id, Launches.objects.filter(id__in=launch_ids_set, parent__isnull=False))))
        launches = Launches.objects.filter(id__in=launch_ids_set, parent__isnull=True).union(Launches.objects.filter(id__in=launch_child_ids_set)).order_by('code')
        return list(launches)

    def do_with__maked_for_grouped(self, maked_for_grouped, model, qty):
        if maked_for_grouped.props.maked_for_grouped.is_set:
            qty += model.objects.filter(id=maked_for_grouped.id, id_f=maked_for_grouped.id_f, parent_id=maked_for_grouped.parent_id).delete()[0]
        else:
            qty += model.objects.filter(id=maked_for_grouped.id, id_f=maked_for_grouped.id, parent_id=None, props=model.props.maked_for_grouped).delete()[0]
            qty += model.objects.filter(id=maked_for_grouped.id, id_f=maked_for_grouped.id_f, parent_id=maked_for_grouped.parent_id).update(
                id_f=maked_for_grouped.id,
                isFolder=False,
                parent_id=None,
                location_ids=F('location_ids_old'),
                exucutors=F('exucutors_old'),
            )
        return qty

    def del_child_maked_for_grouped(self, parent, model, qty=0):
        logger.debug(f'\nparent: {parent}')

        for maked_for_grouped in model.objects.filter(parent_id=parent.id_f):
            qty += self.del_child_maked_for_grouped(parent=maked_for_grouped, model=model, qty=qty)
            qty += self.do_with__maked_for_grouped(maked_for_grouped=maked_for_grouped, model=model, qty=qty)

        return qty

    def ungrouping(self, location_id, launch_ids):
        from kaf_pas.planing.models.production_order_per_launch import Production_order_per_launch
        from kaf_pas.production.models.launches import Launches
        from kaf_pas.planing.models.production_order import Production_order
        from kaf_pas.planing.models.production_order import Production_orderManager

        if launch_ids is not None:
            if isinstance(launch_ids, list):
                launches = map(lambda id: Launches.objects.get(id=id), launch_ids)
            else:
                raise Exception(f'{launch_ids} must be list')
        else:
            launches = list(map(lambda x: Launches.objects.get(id=x.get('launch')), Production_order.objects.all().values('launch').distinct()))

        launches = list(launches)
        qty = 0

        with transaction.atomic():
            for launch in launches:
                if launch.parent is None:
                    model = Production_order
                else:
                    model = Production_order_per_launch

                query = model.objects.filter(location_ids__overlap=[location_id], parent_id=None, launch=launch, props=model.props.maked_for_grouped)
                if query.count() == 0:
                    query = model.objects.filter(location_ids__overlap=[location_id], parent_id__isnull=False, launch=launch)
                    if query.count() > 0:
                        query = model.objects.filter(location_ids__overlap=[location_id], parent_id=None, launch=launch)

                for maked_for_grouped0 in query:
                    qty = self.del_child_maked_for_grouped(parent=maked_for_grouped0, model=model)
                    self.do_with__maked_for_grouped(maked_for_grouped=maked_for_grouped0, model=model, qty=qty)

                for order_production in model.objects.filter(location_ids_old__overlap=[location_id], launch=launch, id=F('id_f'), isFolder=False).exclude(location_ids__overlap=[location_id]):
                    if order_production.parent_id is not None:
                        self.clone_order_production(model=model, id=order_production.id, order_production=order_production, parent_operation_id=None, location=location_id, isFolder=False)
                    else:
                        model.objects.filter(id=order_production.id, id_f=order_production.id_f, parent_id=order_production.parent_id).update(location_ids=F('location_ids_old'))

        if qty > 0:
            for user in self.get_use_4_grouping_message(location_id=location_id):
                Production_orderManager.fullRows(f'_user_id_{user.id}')
        return qty

    def get_launch(self, launch_id=None):
        from kaf_pas.production.models.launches import Launches

        if isinstance(launch_id, int):
            return Launches.objects.get(id=launch_id)
        elif isinstance(launch_id, Launches):
            return launch_id
        else:
            return None

    @classmethod
    def restruct(cls, record, order_model=None):
        from kaf_pas.planing.models.production_order_per_launch import Production_order_per_launch
        from kaf_pas.planing.models.production_order import Production_order
        from kaf_pas.production.models.launches import Launches
        from django.db.models import Model

        if not isinstance(record, dict):
            if isinstance(record, Model):
                record = model_2_dict(record)
            else:
                raise Exception(f'{record} must be dict or django.db.models.Model')
        _record = record.copy()
        setAttr(_record, 'order_model', order_model)

        launch = Launches.objects.get(id=record.get('launch_id'))
        if record.get('parent_id') is None:
            parent_id = None
        else:
            if (order_model is not None and order_model == 'Production_order') or launch.parent is None:
                parent_id = Production_order.objects.get(id_f=record.get('parent_id')).id
            else:
                parent_id = Production_order_per_launch.objects.get(id_f=record.get('parent_id')).id

        if record.get('id_real') is not None:
            setAttr(_record, 'id', record.get('id_real'))
        setAttr(_record, 'parent_id', parent_id)
        return _record

    def grouping1(self, launch_ids):
        from kaf_pas.production.models.launches import Launches
        from kaf_pas.planing.models.production_order import Production_order
        from kaf_pas.ckk.models.locations import Locations
        from kaf_pas.planing.models.production_order_per_launch import Production_order_per_launch

        if isinstance(launch_ids, list):
            launches = filter(lambda x: x.parent is None, map(lambda id: Launches.objects.get(id=id), launch_ids))
        else:
            raise Exception(f'{launch_ids} must be list')

        for launch in launches:
            location_ids = set()

            for location_id in map(lambda production_order: set(production_order.location_ids_old), Production_order.objects.filter(launch=launch)):
                location_ids = location_ids.union(location_id)

            for location in Locations.objects.filter(id__in=location_ids, props=Locations.props.grouping_production_orders).order_by('name'):
                self.grouping(location_id=location.id, launch_id=launch.id)

            location_ids = set()
            for launch_demand in Launches.objects.filter(parent=launch).order_by('code'):
                for location_id in map(lambda production_order: set(production_order.location_ids_old), Production_order_per_launch.objects.filter(launch=launch_demand)):
                    location_ids = location_ids.union(location_id)

                for location in Locations.objects.filter(id__in=location_ids, props=Locations.props.grouping_production_orders).order_by('name'):
                    self.grouping(location_id=location.id, launch_id=launch_demand.id)

    def clone_order_production(self, model, order_production, parent_operation_id, location, isFolder=True, id=None):
        from isc_common.seq import get_deq_next_value
        from kaf_pas.planing.models.production_order import Production_order
        from kaf_pas.planing.models.production_order_per_launch import Production_order_per_launch
        from kaf_pas.ckk.models.locations import Locations

        if not isinstance(order_production, Production_order) and not isinstance(order_production, Production_order_per_launch):
            raise Exception(f'{order_production} must be Production_order or Production_order_per_launch')

        if isinstance(location, int):
            location = Locations.objects.get(id=location)

        parent_dict = model_2_dict(order_production)
        logger.debug(f'\ncloning: {order_production}')

        props = order_production.props
        props |= model.props.maked_for_grouped

        setAttr(parent_dict, 'props', props)
        setAttr(parent_dict, 'location_ids', [location.id])
        setAttr(parent_dict, 'isFolder', isFolder)
        setAttr(parent_dict, 'parent_id', parent_operation_id)

        if id is None:
            id = get_deq_next_value('planing_operations_id_seq')

        setAttr(parent_dict, 'id_f', id)
        if location.id not in order_production.location_ids_old:
            delAttr(parent_dict, 'location_sectors_full_name')
            delAttr(parent_dict, 'location_sectors_ids')

        res = model.objects.create(**parent_dict)
        logger.debug(f'\ncloned order_production: {res}')
        return res

    def get_order_production(self, model, item, launch, location, parent_operation_id=None, level=None):
        from kaf_pas.planing.models.production_order_per_launch import Production_order_per_launch
        from kaf_pas.ckk.models.item_refs import Item_refs

        _launch = launch if issubclass(model, Production_order_per_launch) else launch.parent

        # Сначала ищем в имеющихся раннее сгрупированых позициях с данным parent_operation_id
        query = model.objects.filter(
            location_ids__overlap=[location.id],
            launch=_launch,
            item=item,
            parent_id=parent_operation_id
        )

        cnt = query.count()
        if cnt == 0:
            # Ищем в имеющихся раннее не сгрупированых позициях
            query = model.objects.filter(
                location_ids__overlap=[location.id],
                launch=_launch,
                item=item,
                parent_id=None
            )

            cnt = query.count()
            if cnt == 0:
                # Ищем в имеющихся раннее сгрупированых позициях этого location.id с другим parent_operation_id
                query = model.objects.filter(
                    location_ids__overlap=[location.id],
                    launch=_launch,
                    item=item,
                    parent_id__isnull=False
                )

                cnt = query.count()
                if cnt == 0:
                    # Ищем в позициях всего запуска без учета клонированных
                    query = model.objects.filter(
                        launch=_launch,
                        item=item,
                    ).exclude(props=model.props.maked_for_grouped)
                    cnt = query.count()

                    if cnt == 1:
                        order_production = query[0]

                        isFolder = Item_refs.objects.filter(parent=item, props=Item_refs.props.used).count() > 0
                        if isFolder is True:
                            res = self.clone_order_production(
                                model=model,
                                location=location,
                                order_production=order_production,
                                parent_operation_id=parent_operation_id,
                                isFolder=isFolder)

                            self.restruct_arranges_executors(
                                model=model,
                                parent_id=res.parent_id,
                                launch=res.launch,
                                arranges_exucutors=res.arranges_exucutors,
                                exucutors=res.exucutors
                            )
                            return res
                        else:
                            return None
                    elif cnt == 0:
                        return None
                    else:
                        raise model.MultipleObjectsReturned('<pre>' + '\n\n'.join(list(map(lambda x: str(x), query))) + '</pre>')
                else:
                    order_production = query[0]

                    isFolder = Item_refs.objects.filter(parent=item, props=Item_refs.props.used).count() > 0
                    res = self.clone_order_production(
                        model=model,
                        location=location,
                        order_production=order_production,
                        parent_operation_id=parent_operation_id,
                        isFolder=isFolder)

                    self.restruct_arranges_executors(
                        model=model,
                        parent_id=res.parent_id,
                        launch=res.launch,
                        arranges_exucutors=res.arranges_exucutors,
                        exucutors=res.exucutors
                    )
                    return res
            elif cnt == 1:
                isFolder = Item_refs.objects.filter(parent=item, props=Item_refs.props.used).count() > 0

                res = query[0]

                if len(res.location_ids) == 1 and res.location_ids[0] == location.id and res.parent_id is None:
                    model.objects.filter(id=res.id, id_f=res.id_f, launch=_launch).update(parent_id=parent_operation_id, isFolder=isFolder)
                    res = model.objects.get(id=res.id, id_f=res.id_f, launch=_launch)
                else:
                    location_ids_set = set(res.location_ids)
                    location_ids_set.remove(location.id)

                    model.objects.filter(id=res.id, id_f=res.id_f, launch=_launch).update(location_ids=list(location_ids_set))
                    res = model.objects.get(id=res.id, id_f=res.id_f, launch=_launch)

                    res = self.clone_order_production(
                        model=model,
                        location=location,
                        order_production=res,
                        parent_operation_id=parent_operation_id,
                        isFolder=isFolder)

                self.restruct_arranges_executors(
                    model=model,
                    parent_id=res.parent_id,
                    launch=res.launch,
                    arranges_exucutors=res.arranges_exucutors,
                    exucutors=res.exucutors
                )
                return res
            else:
                raise model.MultipleObjectsReturned('<pre>' + '\n\n'.join(list(map(lambda x: str(x), query))) + '</pre>')
        elif cnt == 1:
            if level == 0:
                if model.objects.filter(parent_id=query[0].id_f).count() > 0:
                    return None

            isFolder = Item_refs.objects.filter(parent=item, props=Item_refs.props.used).count() > 0
            res = query[0]

            model.objects.filter(id=res.id, id_f=res.id_f).update(isFolder=isFolder)
            res = model.objects.filter(id=res.id, id_f=res.id_f)[0]

            return res
        else:
            raise model.MultipleObjectsReturned('<pre>' + '\n\n'.join(list(map(lambda x: str(x), query))) + '</pre>')

    def rec_childs(self, model, parent_item, progreses, location, launch, key, parent_operation=None):
        from kaf_pas.production.models.launch_item_view import Launch_item_view
        from kaf_pas.ckk.models.item import Item

        res = []
        logger.debug(f'\nparent_item:{parent_item}')

        for item_refs in Launch_item_view.objects.filter(parent_id=parent_item.id, launch=launch).exclude(section='Документация'):

            child = Item.objects.get(id=item_refs.id)
            logger.debug(f'\nitem_refs_location.child:{child}')

            order_production = self.get_order_production(
                model=model,
                item=child,
                location=location,
                launch=launch,
                parent_operation_id=parent_operation.id_f if parent_operation is not None else None)

            if order_production is not None:

                _res = self.rec_childs(
                    model=model,
                    location=location,
                    launch=launch,
                    parent_item=child,
                    progreses=progreses,
                    key=key,
                    parent_operation=order_production
                )
                if len(_res) == 0 and order_production.isFolder is True and not location.id in order_production.location_ids_old and order_production.props.maked_for_grouped.is_set:
                    model.objects.filter(id=order_production.id, id_f=order_production.id_f, parent_id=order_production.parent_id, props=model.props.maked_for_grouped).delete()
                elif len(_res) == 0 and order_production.isFolder is True and location.id in order_production.location_ids_old:
                    model.objects.filter(id=order_production.id, id_f=order_production.id_f, parent_id=order_production.parent_id).update(isFolder=False, location_ids=order_production.location_ids_old)
                    order_production = model.objects.get(id=order_production.id, id_f=order_production.id_f, parent_id=order_production.parent_id)
                    res.append(order_production)
                else:
                    res.append(order_production)

            if progreses.step() != 0:
                settings.LOCKS.release(key)
                raise ProgressDroped(progress_deleted)
        return res

    def restruct_arranges_executors(self, model, parent_id, launch, arranges_exucutors, exucutors):

        if parent_id is None:
            return

        try:
            production_order = model.objects.get(id_f=parent_id, launch=launch)
        except model.DoesNotExist as ex:
            raise ex
        except model.MultipleObjectsReturned as ex:
            raise ex

        if production_order.arranges_exucutors is None:
            _arranges_exucutors = set()
        else:
            _arranges_exucutors = set(production_order.arranges_exucutors)

        if arranges_exucutors is not None:
            _arranges_exucutors = _arranges_exucutors.union(set(arranges_exucutors))

        if production_order.exucutors is None:
            _exucutors = set()
        else:
            _exucutors = set(production_order.exucutors)

        _exucutors = _exucutors.union(set(exucutors))

        logger.debug(f'\nproduction_order: {production_order}')

        logger.debug(f'\n_arranges_exucutors: {_arranges_exucutors}')
        logger.debug(f'\narranges_exucutors: {arranges_exucutors}')
        logger.debug(f'\n_exucutors: {_exucutors}')
        logger.debug(f'\nexucutors: {exucutors}')

        model.objects.filter(
            id=production_order.id,
            id_f=production_order.id_f,
            parent_id=production_order.parent_id) \
            .update(arranges_exucutors=list(_arranges_exucutors), exucutors=list(_exucutors))

        self.restruct_arranges_executors(
            model=model,
            parent_id=production_order.parent_id,
            launch=production_order.launch,
            arranges_exucutors=list(_arranges_exucutors),
            exucutors=list(_exucutors)
        )

    def grouping(self, location_id, launch_id=None):
        from kaf_pas.ckk.models.item_refs import Item_refs
        from kaf_pas.ckk.models.locations import Locations
        from kaf_pas.planing.models.production_order import Production_order
        from kaf_pas.planing.models.production_order import Production_orderManager
        from kaf_pas.planing.models.production_order_per_launch import Production_order_per_launch
        from kaf_pas.production.models.launches import Launches

        users = self.get_use_4_grouping_message(location_id=location_id)
        location = Locations.objects.get(id=location_id)

        if launch_id is not None:
            if isinstance(launch_id, int):
                launches = list(Launches.objects.filter(id=launch_id, status__code=in_production).order_by('code'))
                if len(launches) == 0:
                    raise Exception(f'Нет выбора.')

                if launches[0].parent is not None:
                    model = Production_order_per_launch
                else:
                    model = Production_order
                    launches = list(Launches.objects.filter(parent_id=launch_id, status__code=in_production).order_by('code'))

            else:
                raise Exception(f'{launch_id} must be int')
        else:
            model = Production_order
            launches = Launches.objects.filter(parent_id__isnull=False, status__code=in_production).order_by('code')

        key = f'grouping_{location_id}'
        not_founded = Stack()

        # print(f'location_id: {location_id} sz:{sz}')
        for launch in launches:

            settings.LOCKS.acquire(key)
            step = 0

            message = f'Группировка: {location.full_name} Запуск: {launch.code} от {DateToStr(launch.date)}'

            qty = Item_refs.objects.get_descendants_count(id=launch.item.id)

            with managed_progreses(
                    id=key,
                    qty=qty,
                    users=users,
                    message=message,
                    title='Выполнено',
                    props=TurnBitOn(0, 0)
            ) as progreses:
                with transaction.atomic():
                    def except_func():
                        settings.LOCKS.release(key)

                    progreses.except_func = except_func
                    res = []

                    child = launch.item
                    logger.debug(f'\nlaunch.item: {launch.item}')

                    order_production = self.get_order_production(
                        model=model,
                        item=child,
                        location=location,
                        launch=launch,
                        level=0
                    )

                    if order_production is not None:
                        res = self.rec_childs(
                            model=model,
                            parent_item=child,
                            location=location,
                            launch=launch,
                            key=key,
                            parent_operation=order_production,
                            progreses=progreses
                        )

                        if len(res) == 0 and order_production and order_production.isFolder is True:
                            model.objects.filter(id=order_production.id, id_f=order_production.id_f, parent_id=order_production.parent_id, props=model.props.maked_for_grouped).delete()

                        if progreses.step() != 0:
                            settings.LOCKS.release(key)
                            raise ProgressDroped(progress_deleted)

                        step = 1

            settings.LOCKS.release(key)
            if step > 0:
                for user in users:
                    Production_orderManager.fullRows(f'_user_id_{user.id}')

        logger.debug('Done.')

        if not_founded.size() > 0:
            not_founded_str = '<br/>'.join(not_founded)
            settings.EVENT_STACK.EVENTS_PRODUCTION_ORDER_GROUPING.send_message(not_founded_str)

    def check_selected_order_4_finish(self, data, user):
        from kaf_pas.planing.models.production_order_values_ext import Production_orderWrapper
        from kaf_pas.planing.models.production_order_tmp import Production_order_tmp
        from kaf_pas.ckk.models.item import ItemManager

        order_model = data.get('order_model')
        if order_model is None:
            raise Exception('Нет данных по order_model')
        errors = ProductionOrderErrorStack()

        process = data.get('process')

        records = list(map(lambda record: self.restruct(record=record, order_model=order_model), Production_order_tmp.objects.
                           filter(process=process, value_made__isnull=False).
                           exclude(value_made=0).
                           exclude(props=Production_order_tmp.props.qty_not_editing)))

        for record in records:
            setAttr(record, 'order_model', order_model)
            record = Production_orderWrapper(**record)

            # _qty = record.value_made * record.parent_mul
            _qty = record.value_made

            if record.location_sector_ids is not None:
                childs = self.get_enabled_childs(
                    id=record.id,
                    launch=record.launch,
                    user=user,
                    in_dict=False
                )

                if len(childs) > 0 and record.value_start is None:
                    errors.push(ItemManager.getRecord(record.item), 'Не запущено.')
                elif len(childs) > 0 and record.value_odd < _qty:
                    errors.push(ItemManager.getRecord(record.item), f'Не хватает остатка ({record.value_odd}), затребовано {_qty}')
                else:
                    for order_oper in childs:
                        if record.color is None and order_oper.production_operation_attrs is not None and 'color' in order_oper.production_operation_attrs:
                            errors.push(ItemManager.getRecord(record.item), f'Операция: {order_oper.production_operation.full_name} предпологает выбор цвета')

                        if record.launch_incom is None and order_oper.production_operation_is_launched and len(record.child_launches) > 1:
                            errors.push(ItemManager.getRecord(record.item), f'Операция: {order_oper.production_operation.full_name} предпологает выбор запуска')

        return errors.stack

    one = ToDecimal(1)

    def get_FinishFormType(self, data, user, with_out_view=False):
        from kaf_pas.ckk.models.locations_users import Locations_users
        from kaf_pas.planing.models.production_order_opers import Production_order_opers
        from kaf_pas.planing.models.production_order_opers_per_launch import Production_order_opers_per_launch
        from kaf_pas.planing.models.production_order_per_launch import Production_order_per_launch
        from kaf_pas.planing.models.production_order_tmp import Production_order_tmp
        from kaf_pas.planing.models.production_order_tmp import Production_order_tmpManager
        from kaf_pas.production.models.operation_executor import Operation_executor
        from kaf_pas.planing.models.production_order_values_ext import Production_orderWrapper
        from kaf_pas.planing.models.production_order import Production_order
        from kaf_pas.accounting.models.buffer_ext import Buffer_ext

        production_order_ids = Stack()
        buffer_ext = Buffer_ext()

        location_id = data.get('location_id')
        key_process = data.get('key_process')
        records = data.get('records')
        qty_income = data.get('qty')

        # if key_process is not None:
        #     try:
        #         process = Last_used_processes.objects.get(key=key_process, user=request.user).process
        #     except Last_used_processes.DoesNotExist:
        #         process = Production_order_tmpManager.get_process_id()
        #         Last_used_processes.objects.update_or_create(process=process, key=key_process, user=request.user)
        # else:
        process = Production_order_tmpManager.get_process_id()

        if not isinstance(records, list):
            raise Exception(f'{records} must be list')

        has_color = None
        color_id = None
        has_launched = None
        production_items = Stack()

        launches = self.get_main_launches(records=records)

        if len(launches) > 1:
            _str = '\n'.join(map(lambda x: f'№ {x.code} от {DateTimeToStr(x.date)}', launches))
            raise Exception(f'<pre>Недопустимый выбор, сразу из двух главных ветвей запусков: \n{_str}</pre>')

        records = set(map(lambda record: HashableProdOrder(
            id=record.get('id'),
            id_f=record.get('id_f'),
            launch_id=record.get('launch_id'),
            isFolder=record.get('isFolder')), records))

        order_model = None
        order_opers_model = None

        qty = 0
        for record in records:
            if record.launch.parent is None:
                order_model = Production_order
                order_opers_model = Production_order_opers
            else:
                order_model = Production_order_per_launch
                order_opers_model = Production_order_opers_per_launch

            qty += order_model.tree_objects.get_descendants_count(
                id=record.id_f,
                child_id='id_f',
                parent_id='parent_id',
                where_clause1=f'where location_ids && array [{location_id}::bigint] and exucutors && array [{user.id}::bigint] and launch_id={record.launch.id}',
            )

        with managed_progress(
                id=f'get_FinishFormType_{user.id}',
                qty=qty,
                user=user,
                message=f'Подготовка данных',
                title='Выполнено',
                props=TurnBitOn(0, 0)
        ) as progress:
            for record in records:

                if record.launch.parent is None:
                    order_model = Production_order
                    order_opers_model = Production_order_opers
                else:
                    order_model = Production_order_per_launch
                    order_opers_model = Production_order_opers_per_launch

                parent_item_ref_query = order_model.tree_objects.get_descendants(
                    id=record.id_f,
                    child_id='id_f',
                    parent_id='parent_id',
                    where_clause1=f'where location_ids && array [{location_id}::bigint] and exucutors && array [{user.id}::bigint] and launch_id={record.launch.id}',
                    order_by_clause='order by level asc'
                )

                for parent_item_ref in parent_item_ref_query:

                    logger.debug(f'\nparent_item_ref: {parent_item_ref}')
                    progress.setContentsLabel(content=blinkString(f'Подготовка данных: {parent_item_ref.item.item_name}', blink=False, bold=True))

                    try:
                        if parent_item_ref.parent_id is None or parent_item_ref.level == 1:
                            parent_mul = self.one
                        else:
                            _, parent_mul = production_items.find_one(lambda x: x[0] == parent_item_ref.parent_id)
                    except StackElementNotExist:
                        parent_mul = self.one

                    try:
                        p = production_items.find_one(lambda x: x[0] == parent_item_ref.id)
                        if parent_item_ref.level != 1:
                            parent_mul *= sum(parent_item_ref.value1_sum)
                            if p[1] != parent_mul:
                                _production_items = production_items.find(lambda x: x[0] != parent_item_ref.id)
                                production_items.clear()
                                production_items.extend(_production_items)
                                production_items.push((parent_item_ref.id, parent_mul))

                                p = production_order_ids.find_one(lambda element: element.record.id == parent_item_ref.id)
                                p.parent_mul = parent_mul
                                p.level = parent_item_ref.level

                                _production_order_ids = production_order_ids.find(lambda element: element.record.id != parent_item_ref.id)
                                production_order_ids.clear()
                                production_order_ids.extend(_production_order_ids)
                                production_order_ids.push(p)

                                continue
                    except StackElementNotExist:
                        if parent_item_ref.level == 1:
                            production_items.push((parent_item_ref.id, self.one))
                        else:
                            parent_mul *= sum(parent_item_ref.value1_sum)
                            production_items.push((parent_item_ref.id, parent_mul))

                    location_ids = list(set(map(lambda x: x.location.id, Locations_users.objects.filter(user=user))))
                    if parent_item_ref.location_sector_ids is None:
                        parent_item_ref.location_sector_ids = []
                    enabled = len(set(parent_item_ref.location_sector_ids).intersection(set(location_ids))) > 0
                    if enabled is False:
                        production_operations = map(lambda x: x.production_operation, order_opers_model.objects.filter(parent_id=record.id))
                        enabled = Operation_executor.objects.filter(operation__in=production_operations, user=user).count() > 0

                    if enabled is True:
                        from kaf_pas.planing.models.status_operation_types import Status_operation_types
                        statuses = list(map(lambda x: x.id, Status_operation_types.objects.exclude(code__in=[new, closed, doing])))
                        for location_id, status_id in parent_item_ref.location_status_ids.items():
                            enabled = status_id in statuses
                            if enabled is True:
                                break

                    if enabled is False:
                        if not production_order_ids.exists(lambda element: element.record.id == parent_item_ref.id and element.record.launch.id == parent_item_ref.launch.id):
                            production_order_ids.push(Element(
                                enabled=enabled,
                                color_id=color_id,
                                has_color=has_color,
                                has_launched=has_launched,
                                level=parent_item_ref.level,
                                parent_mul=parent_mul,
                                process=process,
                                record=parent_item_ref,
                            ))

                    if parent_item_ref.location_sector_ids is not None:
                        childs = self.get_enabled_childs(
                            id=parent_item_ref.id,
                            launch=parent_item_ref.launch,
                            user=user,
                            in_dict=False
                        )

                        for child in childs:
                            if has_color is True and has_launched is True:
                                break

                            if child.production_operation_attrs is not None and 'color' in child.production_operation_attrs:
                                has_color = True
                                color_id = child.production_operation_color_id
                                if with_out_view is True:
                                    raise Exception('Выполнение требует введение цвета. Режим без просмотра не подходит')

                            if child.production_operation_is_launched is True and len(parent_item_ref.child_launches) > 0:
                                has_launched = True
                                if with_out_view is True:
                                    raise Exception('Выполнение требует введение запуска. Режим без просмотра не подходит')

                        if len(childs) > 0:
                            if not production_order_ids.exists(lambda element: element.record.id == parent_item_ref.id and element.record.launch.id == parent_item_ref.launch.id):
                                production_order_ids.push(Element(
                                    childs=childs,
                                    color_id=color_id,
                                    has_color=has_color,
                                    has_launched=has_launched,
                                    level=parent_item_ref.level,
                                    parent_mul=parent_mul,
                                    process=process,
                                    record=parent_item_ref,
                                    absorption_operation=list(filter(lambda x: x.production_operation_is_absorption is True, childs))
                                ))

                    if progress.step() != 0:
                        raise ProgressDroped(progress_deleted)

            if qty_income is None and with_out_view is True:
                import time
                time.sleep(2)

        if production_order_ids.size() == 0:
            raise Exception(f'Операции не найдены.')

        step = 0
        for production_order in production_order_ids:
            record = production_order.rec
            delAttr(record, 'id')
            delAttr(record, 'max_level')
            delAttr(record, 'location_values_made')
            delAttr(record, 'location_sectors_ready')

            if production_order.absorption_operation is not None and len(production_order.absorption_operation) > 1:
                raise Exception('Наличие более одной операции поглощения.')
            elif production_order.absorption_operation is not None and len(production_order.absorption_operation) == 1:
                total_qty = buffer_ext.get_complect_total_qty(
                    item_id=production_order.record.item.id,
                    launch_id=production_order.record.launch.id,
                    location_id=production_order.childs[step].location.id
                )

                if production_order.record.value_start == 0:
                    raise Exception(f'{production_order.record.item.item_name} : нет запуска.')

                if total_qty > production_order.record.value_start:
                    total_qty = production_order.record.value_start

                if total_qty > 0:
                    def set_demand(_record, _complect):
                        from kaf_pas.sales.models.demand import Demand
                        demand_id = _complect.get('demand_id')
                        if demand_id is not None:
                            demand = Demand.objects.get(id=demand_id)
                            setAttr(_record, 'demand_codes_str', demand.code)
                            setAttr(_record, 'demand_ids', [demand.id])
                        else:
                            delAttr(_record, 'demand_codes_str')
                        return _record

                    complects = buffer_ext.get_launches_complects(
                        total_qty=total_qty,
                        item_id=production_order.record.item.id,
                        launch_id=production_order.record.launch.id,
                        location_id=production_order.childs[0].location.id,
                        with_out_view=with_out_view
                    )

                    for complect in complects:
                        setAttr(record, 'launch_id', complect.get('launch_id'))
                        setAttr(record, 'location_id', complect.get('location_id'))
                        setAttr(record, 'resource_id', complect.get('resource_id'))
                        setAttr(record, 'launch_incom_id', complect.get('launch_id'))
                        setAttr(record, 'value_made', complect.get('complect_qty'))
                        setAttr(record, 'value_made_old', complect.get('complect_qty'))
                        setAttr(record, 'edizm', self.edizm_shtuka)

                        record = set_demand(_record=record, _complect=complect)

                        production_order_tmp = Production_order_tmp.objects.create(**record)
                        production_order_tmp.props |= Production_order_tmp.props.absorption
                        production_order_tmp.id_f += production_order_tmp.id
                        production_order_tmp.save()

                        id_f = production_order_tmp.id_f

                        for item in complect.get('items'):
                            record_item = record.copy()

                            setAttr(record_item, 'color_id', item.color_id)
                            setAttr(record_item, 'edizm', self.edizm_shtuka)
                            setAttr(record_item, 'item_id', item.item_id)
                            setAttr(record_item, 'last_tech_operation_id', item.last_tech_operation_id)
                            setAttr(record_item, 'launch_id', item.launch_id)
                            setAttr(record_item, 'launch_incom_id', item.launch_id)
                            setAttr(record_item, 'location_id', item.location_id)
                            setAttr(record_item, 'parent_id', id_f)
                            setAttr(record_item, 'resource_id', item.resource_id)
                            setAttr(record_item, 'value1_sum', [item.value1_sum])
                            setAttr(record_item, 'value_made', item.value_used)
                            setAttr(record_item, 'value_made_old', item.value_used)
                            setAttr(record_item, 'value_start', item.value_start)
                            setAttr(record_item, 'value_sum', item.value_sum)

                            record_item = set_demand(_record=record_item, _complect=item.__dict__)

                            delAttr(record_item, 'location_sectors_full_name')
                            delAttr(record_item, 'locations_sector_full_name')

                            production_order_tmp = Production_order_tmp.objects.create(**record_item)
                            production_order_tmp.id_f += production_order_tmp.id
                            production_order_tmp.props |= Production_order_tmp.props.absorption
                            production_order_tmp.props |= Production_order_tmp.props.qty_not_editing
                            production_order_tmp.save()
                else:
                    production_order_tmp = Production_order_tmp.objects.create(**record)
                    logger.debug(f'\n{production_order_tmp}')
            elif production_order.has_launched:

                operation = Production_orderWrapper(**self.restruct(record))
                operations_opers = self.get_enabled_childs(id=operation.id, launch=operation.launch, user=user)
                launches = self.get_launches(operations=operations_opers, launch=operation.launch)

                launches_odd = []
                ids = []
                for launch in launches:
                    setAttr(record, 'value_made', launch.get('value_odd_d'))
                    setAttr(record, 'value_made_old', launch.get('value_odd_d'))
                    setAttr(record, 'edizm', Ed_izm.objects.get(code=sht))
                    setAttr(record, 'launch_incom_id', launch.get('id'))

                    production_order_tmp = Production_order_tmp.objects.create(**record)
                    ids.append(production_order_tmp.id)
                    logger.debug(f'\n{production_order_tmp}')

                    launch_odd = dict()
                    setAttr(launch_odd, 'launch_id', launch.get('id'))
                    setAttr(launch_odd, 'value_odd', launch.get('value_odd_d'))
                    launches_odd.append(launch_odd)

                if len(launches_odd) > 0:
                    Production_order_tmp.objects.filter(id__in=ids).update(launches_odd=launches_odd)

            else:
                production_order_tmp = Production_order_tmp.objects.create(**record)
                logger.debug(f'\n{production_order_tmp}')
            step += 1

        # if Production_order_tmp.objects.filter(process=process, status__code=started).count() == 0:
        #     raise Exception('В выборе нет запущенных позиций')

        return dict(
            process=process,
            order_model=order_model.__name__ if order_model else None,
            order_opers_model=order_opers_model.__name__ if order_opers_model else None,
        )

    def get_setFinishStatus(self, data, user):
        from kaf_pas.planing.models.production_order_tmp import Production_order_tmp
        from kaf_pas.planing.models.production_order_values_ext import Production_order_values_ext

        production_order_values_ext = Production_order_values_ext()
        process = data.get('process')
        create_date = StrToDate(data.get('date'))
        order_model = data.get('order_model')

        errors = self.check_selected_order_4_finish(data=data, user=user)

        if len(errors) > 0:
            errors_strs = []
            for error in errors:
                s1 = '\n' + "\n".join(error[1])
                s = f'Для {error[0].item.item_name} выявлены следующие ошибки: {s1}'
                errors_strs.append(s)

            s = '\n\n'.join(errors_strs)
            raise Exception(f'<pre>{s}</pre>')

        with transaction.atomic():
            try:
                records = list(Production_order_tmp.objects.
                               filter(process=process, value_made__isnull=False).
                               exclude(value_made=0).
                               exclude(props=Production_order_tmp.props.qty_not_editing).
                               order_by('-level'))

                res = production_order_values_ext.blockMakeAll1(
                    data=dict(records=records),
                    create_date=create_date,
                    user=user,
                    order_model=order_model
                )
                return res
            except:
                return []

    def get_setStartStatus(self, data, user):
        from kaf_pas.ckk.models.locations_users import Locations_users
        from kaf_pas.planing.models.production_order import Production_order
        from kaf_pas.planing.models.production_order import Production_orderManager
        from kaf_pas.planing.models.production_order import Production_orderQuerySet
        from kaf_pas.planing.models.production_order_per_launch import Production_order_per_launch
        from kaf_pas.planing.models.production_order_values_ext import Production_orderWrapper

        location_id = data.get('location_id')
        qty = None
        if data.get('qty') is not None:
            qty = ToDecimal(data.get('qty'))
        records = data.get('records')

        _res = StackWithId(raise_on_dublicate=False)

        if user.is_admin:
            raise Exception('Операция внесения данных по запуску не работает из режима Администратора.')

        production_order_ids = Stack()
        production_items = Stack()

        with transaction.atomic():
            operation_executor_stack = Operation_executor_stack()
            for record in records:

                record = Production_orderWrapper(**record)
                key = 'get_setStartStatus'

                parent_item_ref_query = Production_order.tree_objects.get_descendants(
                    id=record.id_f,
                    child_id='id_f',
                    where_clause=f'where location_ids && array [{location_id}::bigint] and launch_id={record.launch.id} and "isFolder" = {record.isFolder}',
                    where_clause1=f'where launch_id={record.launch.id} and opertype_id in ({settings.OPERS_TYPES_STACK.PRODUCTION_TASK.id}) and exucutors && array[{user.id}::bigint]',
                )
                settings.LOCKS.acquire(key)

                with managed_progress(
                        id=key,
                        qty=len(list(parent_item_ref_query)),
                        user=user,
                        message='Внесение данных по запуску',
                        title='Выполнено',
                        props=TurnBitOn(0, 0)
                ) as progress:

                    def except_func():
                        settings.LOCKS.release(key)

                    progress.except_func = except_func
                    for parent_item_ref in parent_item_ref_query:
                        qty_in = qty
                        if qty is None:
                            qty_in = parent_item_ref.value_sum

                        if parent_item_ref.launch.parent is None:
                            model = Production_order
                        else:
                            model = Production_order_per_launch

                        progress.setContentsLabel(blinkString(text=f'Внесение данных по запуску {parent_item_ref.item.item_name}, количество: {DecimalToStr(qty_in)}', blink=False, color=black, bold=True))

                        if production_order_ids.exists(lambda x: x == parent_item_ref.id):
                            settings.LOCKS.release(key)
                            break

                        production_order_ids.push(record.id)
                        try:
                            if parent_item_ref.parent_id is None or production_items.size() == 0:
                                parent_mul = 1
                            else:
                                _, parent_mul = production_items.find_one(lambda x: x[0] == parent_item_ref.parent_id)
                        except StackElementNotExist:
                            parent_mul = 1

                        if production_items.size() == 0:
                            _qty = qty_in
                            production_items.push((parent_item_ref.id_f, 1))
                        else:
                            if qty is not None:
                                _qty = qty_in * parent_mul * sum(parent_item_ref.value1_sum)
                            else:
                                _qty = qty_in
                            production_items.push((parent_item_ref.id_f, parent_mul * sum(parent_item_ref.value1_sum)))

                        if isinstance(parent_item_ref.location_sector_ids, list) and parent_item_ref.location_sector_ids[0] in list(map(lambda x: x.location.id, Locations_users.objects.filter(user=user))):
                            _res.push(self.start(
                                _data=self.delete_underscore_element(model_2_dict(parent_item_ref)),
                                qty=_qty,
                                user=user,
                                operation_executor_stack=operation_executor_stack,
                                lock=False,
                                launch=parent_item_ref.launch,
                                model=model
                            ))

                            # Заносим выполнение на это количество

                        if progress.step() != 0:
                            raise ProgressDroped(progress_deleted)

            if _res.size() > 0:
                ids = list(set(map(lambda x: x.get('id'), _res.stack)))
                ids1 = list(set(map(lambda x: HashableProdOrder(id=x.get('id'), launch_id=x.get('launch_id')), _res.stack)))
                location_ids = Production_orderQuerySet.get_user_locations(user=user)

                location_ids = list(set(location_ids))

                for operation_executor in operation_executor_stack.stack:
                    location_ids = list(set(location_ids))
                    if operation_executor.executor.id != user.id:
                        # settings.EVENT_STACK.EVENTS_PRODUCTION_ORDER_CREATE.send_message(
                        #     message=blinkString(f'<h4>Вам направлено: {operation_executor.qty} новых заданий на производство.</h4>', bold=True),
                        #     users_array=[operation_executor.executor],
                        # )
                        # Production_orderManager.refresh_all(
                        #     ids=ids,
                        #     user=operation_executor.executor
                        # )

                        for id1 in ids1:
                            self.updateModelRow(
                                id=id1.id,
                                launch_id=id1.launch.id,
                                location_ids=location_ids,
                                model=model,
                                user=operation_executor.executor,
                            )
                        Production_orderManager.refreshRows(ids=ids, model=model, user=operation_executor.executor, location_ids=location_ids)
                settings.LOCKS.release(key)
            else:
                settings.LOCKS.release(key)
                raise Exception(f'В выборе нет товарнных позиций, которым Вы моглы бы назначить данные по запуску.')
        return _res.stack

    def updateModelRow(self, id, launch_id, model, location_ids, user, status=None, id_f=None, update_ready_struct=False):
        from isc_common.json import StrToJson
        from kaf_pas.planing.models.status_operation_types import Status_operation_types

        location_sector_ids = ExecuteStoredProc('get_location_sector_ids', [id, location_ids])
        if isinstance(location_sector_ids, list):
            location_sector_ids = list(set(location_sector_ids))

        if location_ids is None and location_sector_ids is None:
            return

        location_sectors_full_name = ExecuteStoredProc('get_location_sectors_full_name', [id, location_ids])
        location_status_colors = StrToJson(ExecuteStoredProc('get_location_sector_status_colors', [id, location_ids]))
        location_status_ids = StrToJson(ExecuteStoredProc('get_location_sector_status_ids', [id, location_ids]))
        location_statuses = StrToJson(ExecuteStoredProc('get_location_sector_statuses', [id, location_ids]))
        location_values_made = StrToJson(ExecuteStoredProc('get_location_sector_status_values_made', [id, location_ids]))
        locations_sector_full_name = StrToJson(ExecuteStoredProc('get_locations_sector_full_name', [id, location_ids]))
        value_made = ToDecimal(ExecuteStoredProc('get_operations_values_sum', [id, 'RELEASE_TSK_PLS', None, launch_id]))
        value_start = ToDecimal(ExecuteStoredProc('get_operations_values_sum', [id, 'LAUNCH_TSK', None, launch_id]))
        value_odd = value_start - value_made

        user_ready_struct = None
        if update_ready_struct is True:
            user_ready_struct = User_ready_struct(
                id=id,
                id_f=id_f,
                location_ids=location_ids,
                location_sector_ids=location_sector_ids,
                stack=User_ready_Stack(),
                table_name_tbl=model._meta.db_table,
            )
            self.set_ready_up(user=user, model=model, user_ready_struct=user_ready_struct)

        # if issubclass(model, Production_order):
        #     value_sum = ToDecimal(ExecuteStoredProc('get_operations_values_sum', [id, 'DETAIL_SUM_PRD_TSK', 'is_bit_on(planing_operation_value.props, 0) = false', launch_id]))
        #     value1_sum = ExecuteStoredProc('get_operations_values_sum4', [id, 'DETAIL_SUM_PRD_TSK', 'is_bit_on(planing_operation_value.props, 0) = true', launch_id])
        # elif issubclass(model, Production_order_per_launch):
        #     value_sum = ToDecimal(ExecuteStoredProc('get_operations_values_sum3', [id, 'DETAIL_SUM_PRD_TSK', 'is_bit_on(planing_operation_value.props, 0) = false', launch_id]))
        #     value1_sum = ExecuteStoredProc('get_operations_values_sum3', [id, 'DETAIL_SUM_PRD_TSK', 'is_bit_on(planing_operation_value.props, 0) = true', launch_id])
        # else:
        #     raise Exception(f'{model} must be Production_order or Production_order_per_launch')

        res = dict(
            location_sector_ids=list(set(location_sector_ids)) if location_sector_ids is not None else None,
            location_sectors_full_name=location_sectors_full_name,
            location_status_colors=location_status_colors,
            location_status_ids=location_status_ids,
            location_statuses=location_statuses,
            location_values_made=location_values_made,
            locations_sector_full_name=locations_sector_full_name,
            # value1_sum=value1_sum,
            value_made=value_made,
            value_start=value_start,
            value_odd=value_odd,
            # value_sum=value_sum,
        )

        if status is not None:
            if isinstance(status, int):
                setAttr(res, 'status_id', status)
            elif isinstance(status, Status_operation_types):
                setAttr(res, 'status', status)

        model.objects.filter(id=id).update(**res)
        return user_ready_struct

    def log_list(self, lst):
        if isinstance(lst, list):
            if len(lst) == 0:
                logger.debug('[]')

            idx = 1
            for item in lst:
                logger.debug(f'{idx}: {item}')
                idx += 1

    def get_ready(self, id, location_ids, model, user):
        if location_ids is not None and len(location_ids) > 0:
            location_sectors_ready = StrToJson(ExecuteStoredProc('get_location_sectors_ready', [id, location_ids]))

            location_sectors_ready = delNonePropFromDict(location_sectors_ready)

            keys = list(map(lambda x: ToInt(x), location_sectors_ready.keys()))
            location_not_in = list(set(location_ids).difference(set(filter(lambda x: x is not None, keys))))

            if len(location_not_in) > 0:
                from kaf_pas.production.models.operation_executor import Operation_executor
                operation_executor_ids = map(lambda x: x.operation.id, Operation_executor.objects.filter(user=user))
                operation_ids = list(map(lambda x: x.production_operation.id, model.all_childs(id=id).filter(production_operation_id__in=operation_executor_ids)))
                if len(operation_ids) > 0:
                    ready1 = StrToJson(ExecuteStoredProc('get_user_operation_ready1', [id, operation_ids]))
                    location_sectors_ready.update(ready1)

            return delNonePropFromDict(location_sectors_ready)

    def _rec_rows1(self, rows1, user_ready_struct, user, model, locations_sector_ready_nz, location_sectors_ready, progress=None, key=None, for_first_ready=False):
        for row1 in rows1:
            id1, id_f1, parent_id, isFolder, location_ids1, _ = row1
            try:
                item = user_ready_struct.stack.find_one(id=id1)
                logger.debug(f'Finded: {item}')
            except StackElementNotExist:
                user_ready_struct_child = User_ready_struct(
                    id=id1,
                    id_f=id_f1,
                    location_ids=location_ids1,
                    stack=user_ready_struct.stack,
                    table_name_tbl=user_ready_struct.table_name_tbl,
                )
                location_sectors_ready = self.check_user_ready_down(
                    user_ready_struct=user_ready_struct_child,
                    user=user,
                    key=key,
                    model=model
                )
                locations_sector_ready_nz.update(delZeroPropFromDict(location_sectors_ready))
                logger.debug(f'Out: {user_ready_struct_child}')

            if progress is not None and progress.step() != 0:
                settings.LOCKS.release(key)
                raise ProgressDroped(progress_deleted)

            if for_first_ready is True:
                for location_id, ready in locations_sector_ready_nz.items():
                    if ready == 1:
                        return location_sectors_ready, locations_sector_ready_nz, True

        return location_sectors_ready, locations_sector_ready_nz, False

    def check_user_ready_down(self, user_ready_struct, user, model, key=None, for_first_ready=False):
        from isc_common.auth.models.user import User
        from kaf_pas.ckk.models.locations import Locations

        if user_ready_struct.id_f is None:
            user_ready_struct.id_f = model.objects.filter(id=user_ready_struct.id)[0].id_f

        if isinstance(user, int):
            user = User.objects.get(id=user)

        if model is None:
            raise Exception('model dont be None')

        logger.debug(f'In: {user_ready_struct}')

        def sql_str(table_name):
            res = delete_dbl_spaces(f'''SELECT id, id_f, parent_id, "isFolder", location_ids, location_sectors_ready
                       FROM {table_name}
                       WHERE parent_id = %s''')
            # logger.debug(f'\nres: {res}\n')
            return res

        with connection.cursor() as cursor:
            cursor.execute(sql_str(table_name=user_ready_struct.table_name_tbl), [user_ready_struct.id_f])
            rows1 = cursor.fetchall()
            rows1.sort()
            self.log_list(rows1)

            if len(rows1) == 0:
                location_sectors_ready = dict()
                if user_ready_struct.location_ids is not None and len(user_ready_struct.location_ids) > 0:
                    location_sectors_ready = self.get_ready(
                        id=user_ready_struct.id,
                        location_ids=user_ready_struct.location_ids,
                        model=model,
                        user=user,
                    )

                user_ready_struct.stack.push(dict(id=user_ready_struct.id, location_sectors_ready=location_sectors_ready))
                return location_sectors_ready

            locations_sector_ready_nz = dict()

            li = user_ready_struct.location_sector_ids if user_ready_struct.location_sector_ids is not None else user_ready_struct.location_ids
            if li is None:
                return

            s = '<br>'.join(list(map(lambda x: x.fullname, Locations.objects.filter(id__in=li))))

            if key is None:
                location_sectors_ready, locations_sector_ready_nz, ex = self._rec_rows1(
                    location_sectors_ready=locations_sector_ready_nz,
                    locations_sector_ready_nz=locations_sector_ready_nz,
                    model=model,
                    rows1=rows1,
                    user=user,
                    user_ready_struct=user_ready_struct,
                    for_first_ready=for_first_ready,
                )

                if ex is True:
                    return location_sectors_ready
            else:
                with managed_progress(
                        id=f'key_{user_ready_struct.id_f}',
                        qty=len(rows1),
                        user=user,
                        message=f'Переcчет готовностей заданий <br>{s}',
                        title='Выполнено',
                        props=TurnBitOn(0, 0)
                ) as progress:
                    location_sectors_ready, locations_sector_ready_nz, exit = self._rec_rows1(
                        key=key,
                        location_sectors_ready=locations_sector_ready_nz,
                        locations_sector_ready_nz=locations_sector_ready_nz,
                        model=model,
                        progress=progress,
                        rows1=rows1,
                        user=user,
                        user_ready_struct=user_ready_struct,
                    )

                    if exit is True:
                        return location_sectors_ready

            if user_ready_struct.location_ids is not None and len(user_ready_struct.location_ids) > 0:
                location_sectors_ready = self.get_ready(
                    id=user_ready_struct.id,
                    location_ids=user_ready_struct.location_ids,
                    model=model,
                    user=user
                )
                location_sectors_ready.update(locations_sector_ready_nz)

                user_ready_struct.stack.push(dict(id=user_ready_struct.id, location_sectors_ready=location_sectors_ready), logger=logger)
                self.update_user_params_down(
                    id=user_ready_struct.id,
                    location_sectors_ready=location_sectors_ready,
                    table_name_tbl=user_ready_struct.table_name_tbl
                )

                return location_sectors_ready
            else:
                raise Exception('Аварийный останов.')

    def set_ready_up(self, user_ready_struct, user, model, location_sectors_ready=None):
        from isc_common.auth.models.user import User
        from kaf_pas.ckk.models.item import Item

        if user_ready_struct.id_f is None:
            user_ready_struct.id_f = model.objects.filter(id=user_ready_struct.id)[0].id_f

        if user_ready_struct.isFolder is None:
            if user_ready_struct.id is not None:
                item = model.objects.filter(id=user_ready_struct.id)[0]
            else:
                item = model.objects.filter(id_f=user_ready_struct.id_f)[0]
            user_ready_struct.isFolder = item.isFolder
            user_ready_struct.item_name = item.item.item_name

        if location_sectors_ready is None:
            location_sectors_ready = self.check_user_ready_down(user_ready_struct=user_ready_struct, model=model, user=user, for_first_ready=True)

        if isinstance(user, int):
            user = User.objects.get(id=user)

        def get_parent(id_f, table_name_tbl):
            with connection.cursor() as cursor:
                cursor.execute(f'''SELECT parent_id
                                   FROM {table_name_tbl}
                                   WHERE id_f = %s''', [id_f])
                parent_id, = cursor.fetchone()
                return parent_id

        def get_parent_struct(parent_id, table_name_tbl):
            with connection.cursor() as cursor:
                cursor.execute(f'''SELECT id, item_id
                                   FROM {table_name_tbl}
                                   WHERE id_f = %s''', [parent_id])
                return cursor.fetchone()

        def get_location_sectors_readies(parent_id, id_f, table_name_tbl):
            with connection.cursor() as cursor:
                sqlstr = f'''SELECT distinct location_sectors_ready
                                 FROM {table_name_tbl}
                                 WHERE parent_id=%s and id_f != %s'''

                cursor.execute(sqlstr, [parent_id, id_f])
                readies = cursor.fetchall()
                readies = list(filter(lambda x: x[0] is not None, readies))

                res = dict()
                readies = list(map(lambda x: StrToJson(x[0]), readies))
                for ready in readies:
                    for k, v in ready.items():
                        if res.get(k) is None:
                            setAttr(res, k, v)
                        elif res.get(k) == 0 and k == 1:
                            setAttr(res, k, v)

                return res

        parent_id = get_parent(id_f=user_ready_struct.id_f, table_name_tbl=user_ready_struct.table_name_tbl)

        if parent_id is None:
            return

        id, item_id = get_parent_struct(parent_id=parent_id, table_name_tbl=user_ready_struct.table_name_tbl)
        item_name = Item.objects.get(id=item_id).item_name

        location_sectors_ready1 = get_location_sectors_readies(
            parent_id=parent_id,
            id_f=user_ready_struct.id_f,
            table_name_tbl=user_ready_struct.table_name_tbl
        )

        location_sectors_ready1.update(location_sectors_ready)

        if user_ready_struct.isFolder is True:
            self.update_user_params_down(
                id=user_ready_struct.id,
                location_sectors_ready=location_sectors_ready,
                table_name_tbl=user_ready_struct.table_name_tbl
            )

            user_ready_struct.stack.push(dict(id=user_ready_struct.id, location_sectors_ready=location_sectors_ready))

        self.update_user_params_down(
            id=id,
            location_sectors_ready=location_sectors_ready1,
            table_name_tbl=user_ready_struct.table_name_tbl
        )

        user_ready_struct.stack.push(dict(id=id, location_sectors_ready=location_sectors_ready))

        user_ready_struct1 = User_ready_struct(
            id=id,
            id_f=parent_id,
            stack=user_ready_struct.stack,
            table_name_tbl=user_ready_struct.table_name_tbl
        )
        self.set_ready_up(user_ready_struct=user_ready_struct1, location_sectors_ready=location_sectors_ready1, model=model, user=user)

    def update_user_params_down(self, id, location_sectors_ready, table_name_tbl):
        if location_sectors_ready is None:
            return

        with connection.cursor() as cursor:
            cursor.execute(f'update "{table_name_tbl}" set location_sectors_ready=%s where id = %s', [JsonToStr(location_sectors_ready), id])

    def create_s_table(self):
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

        from isc_common.common.mat_views import create_insert_update_delete_function_of_table

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

    def fill_locations_sector_ready(self, launch_ids, user):
        from kaf_pas.production.models.launches import Launches

        def sql_top_level_str(table_name, location_id):
            res = f'''SELECT s.id, s.id_f, s.parent_id, s."isFolder", s.location_sectors_ready, s.location_ids
                      FROM {table_name} as s
                      WHERE s.parent_id is null
                        and s."isFolder" = true
                        and s.launch_id in %s
                        and s.location_ids = array [{location_id}]::bigint[]
                        '''

            # logger.debug(f'\nsql_top_level_str: {res}\n')
            return res

        def fill_table(table_name_tbl, launch_ids, progress, key):
            from kaf_pas.planing.models.production_order import Production_order
            from kaf_pas.planing.models.production_order_per_launch import Production_order_per_launch
            from kaf_pas.ckk.models.locations import Locations

            if isinstance(launch_ids, list) and len(launch_ids) == 0:
                return

            with connection.cursor() as cursor:
                for location in Locations.objects.filter(props=Locations.props.grouping_production_orders):
                    cursor.execute(sql_top_level_str(table_name=table_name_tbl, location_id=location.id), [tuple(launch_ids)])
                    rows = cursor.fetchall()
                    rows.sort()

                    stack = StackWithId()
                    self.log_list(rows)
                    progress.setQty(len(rows))
                    # s = f'{progress.message}<br>{location.fullname}'
                    # progress.setContentsLabel(s)

                    for row in rows:
                        id, id_f, parent_id, isFolder, location_sectors_ready, location_ids = row
                        try:
                            item = stack.find_one(id=id)
                            logger.debug(f'Finded: {item}')
                        except StackElementNotExist:
                            user_ready_struct = User_ready_struct(
                                id=id,
                                id_f=id_f,
                                location_ids=location_ids,
                                stack=stack,
                                table_name_tbl=table_name_tbl, )

                            model = None
                            if table_name_tbl == 'planing_production_order_tbl':
                                model = Production_order
                            elif table_name_tbl == 'planing_production_order_per_launch_tbl':
                                model = Production_order_per_launch

                            self.check_user_ready_down(user_ready_struct=user_ready_struct, user=user, key=key, model=model)
                            logger.debug(f'Out: {user_ready_struct}')

                        if progress.step() != 0:
                            settings.LOCKS.release(key)
                            raise ProgressDroped(progress_deleted)

        launch_ids1 = list(map(lambda x: x.id, Launches.objects.filter(id__in=launch_ids, parent=None).exclude(code__in=['Нет'])))
        launch_ids2 = list(map(lambda x: x.id, Launches.objects.filter(id__in=launch_ids, parent__isnull=False)))

        key = '_'.join(map(lambda x: str(x), launch_ids1))
        with managed_progress(
                id=key,
                qty=len(launch_ids1) + len(launch_ids2),
                user=user,
                message='Переcчет готовностей заданий',
                title='Выполнено',
                props=TurnBitOn(0, 0)
        ) as progress:
            with transaction.atomic():
                def except_func():
                    settings.LOCKS.release(key)

                progress.except_func = except_func

                tablename = 'planing_production_order_tbl'
                # table_name_tbl = f'''{tablename}_user'''
                logger.debug(f'Filling: {tablename}')

                fill_table(table_name_tbl=tablename, launch_ids=launch_ids1, progress=progress, key=key)

                logger.debug(f'Filled: {tablename}')

                tablename = 'planing_production_order_per_launch_tbl'
                # table_name_tbl = f'''{tablename}_user'''
                logger.debug(f'Filling: {tablename}')

                fill_table(table_name_tbl=tablename, launch_ids=launch_ids2, progress=progress, key=key)

                logger.debug(f'Filled: {tablename}')

    def refreshRowsProdOrder(self, res_ids, model, user):
        from kaf_pas.planing.models.production_order import Production_orderManager
        from kaf_pas.planing.models.production_order import Production_orderQuerySet

        location_ids = []
        if len(res_ids) > 0:
            location_ids = Production_orderQuerySet.get_user_locations(user=user)

        records = []
        for id, level in res_ids:
            res_query = model.objects.filter(id=id)

            if isinstance(location_ids, list):
                res_query.filter(location_ids=location_ids)
            records.extend(map(lambda record: setAttr(record, 'level', level), res_query.values('id', 'launch_id', 'status')))

        key = 'refreshRowsProdOrder'

        cnt = len(records)
        with managed_progress(
                id=key,
                qty=cnt,
                user=user,
                message=f'Обновление... ({cnt} позиций)',
                title='Выполнено',
                props=TurnBitOn(0, 0)
        ) as progress:

            def except_func():
                settings.LOCKS.release(key)

            progress.except_func = except_func

            _res_ids = []
            for record in records:
                user_ready_struct = self.updateModelRow(
                    id=record.get('id'),
                    launch_id=record.get('launch_id'),
                    location_ids=location_ids,
                    model=model,
                    status=record.get('status'),
                    update_ready_struct=record.get('level') == 1,
                    user=user,
                )
                if user_ready_struct is not None:
                    _res_ids.append(user_ready_struct)

                if progress.step() != 0:
                    settings.LOCKS.release(key)
                    raise ProgressDroped(progress_deleted)

            if len(_res_ids) > 0:
                res_ids = _res_ids

            Production_orderManager.refreshRows(ids=list(map(lambda x: x[0] if isinstance(res_ids, tuple) else x.id, res_ids)), user=user, model=model)
            settings.LOCKS.release(key)
