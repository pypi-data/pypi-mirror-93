import logging

from bitfield import BitField
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import EmptyResultSet
from django.db import connection
from django.db.models import DecimalField, DateTimeField, TextField, BooleanField, BigIntegerField, PositiveIntegerField, SmallIntegerField, Sum

from isc_common import delAttr, setAttr
from isc_common.auth.models.user import User
from isc_common.common import blinkString, sht
from isc_common.datetime import DateTimeToStr
from isc_common.fields.code_field import CodeField, JSONFieldIVC
from isc_common.fields.related import ForeignKeyProtect, ForeignKeyCascade
from isc_common.http.DSRequest import DSRequest
from isc_common.managers.common_manager import CommonManager
from isc_common.models.audit import AuditQuerySet, AuditModel
from isc_common.models.standard_colors import Standard_colors
from isc_common.models.tree_audit import TreeAuditModelManager
from isc_common.number import DecimalToStr, ToDecimal, ToStr, model_2_dict, DelProps
from isc_common.ws.webSocket import WebSocket
from kaf_pas.ckk.models.ed_izm import Ed_izm
from kaf_pas.ckk.models.item import Item
from kaf_pas.ckk.models.locations import Locations
from kaf_pas.planing.models.operation_types import Operation_types
from kaf_pas.planing.models.operations import Operations
from kaf_pas.planing.models.production_order import Production_orderQuerySet, Production_orderManager
from kaf_pas.planing.models.production_order_tmp_ext import Production_order_tmp_ext
from kaf_pas.production.models.launches import Launches
from kaf_pas.production.models.resource import Resource

logger = logging.getLogger(__name__)


class Production_order_tmpQuerySet(AuditQuerySet):
    production_order_tmp_ext = Production_order_tmp_ext()

    def get_Count(self, request):
        request = DSRequest(request=request)
        data = request.get_data()
        return self.production_order_tmp_ext.get_Count(data=data)

    def get_Check(self, request):

        request = DSRequest(request=request)
        data = request.get_data()
        return self.production_order_tmp_ext.get_Check(data=data, user=request.user)

    def set_Count(self, request):
        request = DSRequest(request=request)
        data = request.get_data()

        return self.production_order_tmp_ext.set_Count(data=data, user=request.user)

    def get_range_rows(self, start=None, end=None, function=None, json=None, distinct_field_names=None, user=None, *args, **kwargs):
        from kaf_pas.planing.models.production_order import Production_order
        from kaf_pas.planing.models.production_order_per_launch import Production_order_per_launch
        from kaf_pas.production.models.operation_executor import Operation_executor

        data = json.get('data')

        process = data.get('process')
        if process is None:
            setAttr(json.get('data'), 'process', -1)

        order_model = data.get('order_model')
        order_opers_model = data.get('order_opers_model')

        delAttr(json.get('data'), 'order_model')
        delAttr(json.get('data'), 'order_opers_model')

        queryResult = self._get_range_rows(*args, start=start, end=end, function=function, json=json, distinct_field_names=distinct_field_names)

        try:
            logger.debug(f'\n\n{queryResult.query}\n')
        except EmptyResultSet:
            pass

        location_ids = Production_orderQuerySet.get_user_locations(user=user)
        executor_operation_ids = Operation_executor.executor_operation_ids(user=user)
        model = Production_order if order_model == 'Production_order' else Production_order_per_launch

        res = [function(
            record,
            location_ids,
            user,
            model,
            executor_operation_ids
        ) for record in queryResult]
        return res


class Production_order_tmpManager(CommonManager):
    production_order_tmp = Production_order_tmp_ext()

    def get_queryset(self):
        return Production_order_tmpQuerySet(self.model, using=self._db)

    @classmethod
    def refreshRows(cls, ids, user, model=None):
        from kaf_pas.planing.models.production_order import Production_order
        from kaf_pas.production.models.operation_executor import Operation_executor

        if model is None:
            model = Production_order

        if user is None or (isinstance(ids, list) and len(ids) == 0):
            return

        ids = Production_orderManager.ids_list_2_int_list(ids)

        location_ids = Production_orderQuerySet.get_user_locations(user=user)
        executor_operation_ids = Operation_executor.executor_operation_ids(user=user)

        records = [cls.getRecord(
            record=record,
            location_ids=location_ids,
            user=user,
            model=model,
            executor_operation_ids=executor_operation_ids
        ) for record in Production_order_tmp.objects.filter(id__in=ids)]

        WebSocket.row_refresh_grid(grid_id=f'{settings.GRID_CONSTANTS.refresh_production_order_tmp_grid_row}', records=records)

    @classmethod
    def fullRows(cls, suffix=''):
        WebSocket.full_refresh_grid(grid_id=f'{settings.GRID_CONSTANTS.refresh_production_order_tmp_grid}{suffix}')

    @classmethod
    def props(cls):
        return BitField(flags=(
            ('absorption', 'Для поглощения'),  # 1
            ('qty_not_editing', 'Без возможности правки кол-ва'),  # 2
        ), default=0, db_index=True)

    @classmethod
    def getRecord(cls, record, location_ids, user, model, executor_operation_ids):
        from isc_common.number import Set

        executor_operation_location_ids = Production_orderQuerySet.get_user_locations(user=user)

        record_attrs = Production_orderManager.getRecord_attrs(
            record=record,
            location_ids=location_ids,
            user=user,
            model=model,
            executor_operations_ids=executor_operation_ids,
            executor_operation_location_ids=executor_operation_location_ids,
            tmp=True
        )

        status__name = record_attrs.status__name
        status__color = record_attrs.status__color
        status_id = record_attrs.status_id
        location_sectors_full_name = record_attrs.location_sectors_full_name
        location_sectors_ready = record_attrs.location_sectors_ready
        launch__code = record_attrs.launch__code
        value_made = record_attrs.value_made
        value1_sum = record_attrs.value1_sum
        value1_sum_len = record_attrs.value1_sum_len

        item__STMP_1__value_str = record.item.STMP_1.value_str if record.item.STMP_1 else None
        item__STMP_2__value_str = record.item.STMP_2.value_str if record.item.STMP_2 else None

        res = {
            'arranges_exucutors': sorted(record.arranges_exucutors) if record.arranges_exucutors is not None else None,
            'child_launches': record.child_launches,
            'childs': record.childs,
            'color__color': record.color.color if record.color else None,
            'color__color__color': record.color.color if record.color else None,
            'color__color__name': record.color.name if record.color else None,
            'color__name': record.color.name if record.color else None,
            'color_color': record.color.color if record.color else None,
            'color_id': record.color.id if record.color else None,
            'color_name': record.color.name if record.color else None,
            'creator__short_name': record.creator.get_short_name,
            'creator_short_name': record.creator.get_short_name,
            'date': record.date,
            'demand_codes_str': record.demand_codes_str,
            'demand_ids': record.demand_ids,
            'description': record.description,
            'edizm__name': record.edizm.name if record.edizm else None,
            'edizm_id': record.edizm.id if record.edizm else None,
            'edizm_name': record.edizm.name if record.edizm else None,
            'enabled': record.enabled,
            'exucutors': sorted(record.exucutors),
            'exucutors_old': sorted(record.exucutors_old),
            'has_color': record.has_color,
            'has_launched': record.has_launched,
            'id': record.id,
            'id_f': record.id_f,
            'id_real': record.id_real,
            'isFolder': record.isFolder if record.isFolder is not None else False,
            'item__STMP_1__value_str': item__STMP_1__value_str,
            'item__STMP_2__value_str': item__STMP_2__value_str,
            'item_id': record.item.id,
            'item_STMP_1_value_str': item__STMP_1__value_str,
            'item_STMP_2_value_str': item__STMP_2__value_str,
            'launch__code': launch__code,
            'launch__date': record.launch.date,
            'launch_code': launch__code,
            'launch_date': record.launch.date,
            'launch_id': record.launch.id,
            'launch_incom__code': record.launch_incom.code if record.launch_incom else None,
            'launch_incom__date': record.launch_incom.date if record.launch_incom else None,
            'launch_incom_code': record.launch_incom.code if record.launch_incom else None,
            'launch_incom_date': record.launch_incom.date if record.launch_incom else None,
            'launch_incom_id': record.launch_incom.id if record.launch_incom else None,
            'launches_odd': record.launches_odd,
            'level': record.level,
            'location_ids': record.location_ids,
            'location_ids_old': record.location_ids_old,
            'location_sector_ids': Set(record.location_sector_ids).get_set_sorted_as_original,
            'location_sectors_full_name': location_sectors_full_name,
            'location_sectors_ready': location_sectors_ready,
            'location_values_made': record.location_values_made,
            'num': record.num,
            'qty_not_editing': record.props.qty_not_editing,
            'opertype__full_name': record.opertype.full_name,
            'opertype_id': record.opertype.id,
            'parent_id': record.parent_id,
            'parent_item_id': record.parent_item.id if record.parent_item is not None else None,
            'parent_item_ids': record.parent_item_ids,
            'parent_mul': record.parent_mul,
            'process': record.process,
            'props': record.props,
            'status__code': record.status.code,
            'status__name': blinkString(text=status__name, blink=False, color=status__color, bold=True),
            'status_code': record.status.code,
            'status_id': status_id,
            'status_name': blinkString(text=status__name, blink=False, color=status__color, bold=True),
            'value1_sum': value1_sum,
            'value1_sum_len': value1_sum_len,
            'value_made': DecimalToStr(value_made, noneId_0=True),
            'value_odd': DecimalToStr(record.value_odd, noneId_0=True),
            'value_start': DecimalToStr(record.value_start),
            'value_sum': DecimalToStr(record.value_sum),
        }
        return DelProps(res)

    def updateFromRequest(self, request):
        from kaf_pas.ckk.models.ed_izm import Ed_izm
        from kaf_pas.planing.models.operation_color_view import Operation_color_view

        request = DSRequest(request=request)
        data = request.get_data()
        value_odd = data.get('value_odd')
        value_made = ToDecimal(data.get('value_made'))
        if value_made > ToDecimal(value_odd):
            raise Exception(f'Превышение остатка, возможная величина: {value_odd}')

        id = data.get('id')
        edizm_id = data.get('edizm_id')
        color_id = data.get('color_id')
        item_id = data.get('item_id')

        self.production_order_tmp.update_absorption(id=id, value_made=value_made, user=request.user)

        old_record = Production_order_tmp.objects.get(id=id)

        edizm = None
        if value_made is not None:
            if edizm_id is None:
                edizm = Ed_izm.objects.get(code=sht)
            else:
                if value_made == 0:
                    edizm = None
                else:
                    edizm = Ed_izm.objects.get(id=edizm_id)

        if color_id is not None:
            try:
                color = Standard_colors.objects.get(id=color_id)
            except Standard_colors.DoesNotExist:
                color = Operation_color_view.objects.get(id=color_id).color
        elif old_record.color is not None:
            color = old_record.color
        else:
            color = None

        launch_incom__code = data.get('launch_incom__code')
        launch_incom_id = data.get('launch_incom_id')
        launches_odd = Production_order_tmp.objects.get(id=id).launches_odd

        launch_incom = None
        if launch_incom__code is not None and launch_incom_id is None:
            launch_incom = Launches.objects.get(code=launch_incom__code)
        elif launch_incom_id is not None:
            launch_incom = Launches.objects.get(id=launch_incom_id)
        elif old_record.launch_incom is not None:
            launch_incom = old_record.launch_incom

        v_l = list(filter(lambda x: x.get('launch_id') == launch_incom.id, launches_odd))
        if len(v_l) > 0 and (value_made is None or value_made == 0):
            value_made = v_l[0].get('value_odd')
            setAttr(data, 'value_made', value_made)

            if edizm is None:
                edizm = Ed_izm.objects.get(code=sht)

        if launch_incom is not None and value_made is not None:
            odd = list(filter(lambda x: x.get('launch_id') == launch_incom.id, launches_odd))
            if len(odd) > 0:
                process = Production_order_tmp.objects.get(id=id).process
                odd = odd[0]
                value_made__sum = Production_order_tmp.objects.filter(process=process, launch_incom=launch_incom, item_id=item_id).exclude(id=id).aggregate(Sum('value_made'))
                value_made__sum = value_made__sum.get('value_made__sum')

                if ToDecimal(odd.get('value_odd')) < ToDecimal(value_made) + ToDecimal(value_made__sum):
                    delAttr(data, 'edizm_id')
                    delAttr(data, 'edizm__name')
                    delAttr(data, 'value_made')

                    raise Exception(f'Превищение суммы по запуску ({value_made}), возможная величина: {ToStr(ToDecimal(odd.get("value_odd")) - ToDecimal(value_made__sum))}')

        super().filter(id=id).update(edizm=edizm, value_made=value_made, color=color, launch_incom=launch_incom)

        if edizm is not None:
            setAttr(data, 'edizm_id', edizm.id)
            setAttr(data, 'edizm__name', edizm.name)
        else:
            delAttr(data, 'edizm_id')
            delAttr(data, 'edizm__name')
            delAttr(data, 'value_made')

        if value_made is None or value_made == 0:
            delAttr(data, 'edizm_id')
            delAttr(data, 'edizm__name')
            delAttr(data, 'value_made')

        if color is not None:
            setAttr(data, 'color_id', color.id)
            setAttr(data, 'color__color__name', color.name)
            setAttr(data, 'color__color__color', color.color)
        else:
            delAttr(data, 'color_id')
            delAttr(data, 'color__color__name')
            delAttr(data, 'color__color__color')

        if launch_incom is not None:
            setAttr(data, 'launch_incom_id', launch_incom.id)
            setAttr(data, 'launch_incom__code', launch_incom.code)
            setAttr(data, 'launch_incom__date', launch_incom.date)
        else:
            delAttr(data, 'launch_incom_id')
            delAttr(data, 'launch_incom__code')
            delAttr(data, 'launch_incom__date')

        return data

    def copyFromRequest(self, request):
        request = DSRequest(request=request)
        data = request.get_data()
        production_order_tmp = self.delete_underscore_element(model_2_dict(Production_order_tmp.objects.get(id=data.get('id'))))
        # delAttr(production_order_tmp, 'edizm_id')
        delAttr(production_order_tmp, 'id')
        delAttr(production_order_tmp, 'value_made')
        # delAttr(production_order_tmp, 'color_id')
        # delAttr(production_order_tmp, 'launch_incom_id')
        production_order_tmp = model_2_dict(Production_order_tmp.objects.create(**production_order_tmp))
        Production_order_tmpManager.fullRows()
        return production_order_tmp

    def deleteFromRequest(self, request, removed=None, ):
        from django.db import transaction

        request = DSRequest(request=request)
        res = 0
        tuple_ids = request.get_olds_tuple_ids()
        with transaction.atomic():
            for id, mode in tuple_ids:
                production_order_tmp = Production_order_tmp.objects.get(id=id)
                if production_order_tmp.props.qty_not_editing.is_set is True:
                    raise Exception('Отдельно струки комплектации удалить не могу.')

                with connection.cursor() as cursor:
                    sql_text = '''WITH RECURSIVE r AS (
                                    select s.*
                                    from (SELECT id, id_f, 1 AS level
                                          FROM planing_production_order_tmp
                                          WHERE id = %s
                                         ) as s
                                
                                    union all
                                
                                    SELECT planing_production_order_tmp.id, planing_production_order_tmp.id_f, r.level + 1 AS level
                                    FROM planing_production_order_tmp
                                             JOIN r
                                                  ON planing_production_order_tmp.parent_id = r.id_f)
                                
                                select id
                                from r
                                order by level desc'''
                    cursor.execute(sql_text, [id])
                    rows = cursor.fetchall()
                    for row in rows:
                        _id, = row
                        qty = Production_order_tmp.objects.filter(id=_id).delete()[0]
                res += qty
        return res

    @classmethod
    def get_process_id(cls):
        from isc_common.seq import get_deq_next_value
        return get_deq_next_value('planing_production_order_tmp_id_seq')


class Production_order_tmp(AuditModel):
    from kaf_pas.planing.models.status_operation_types import Status_operation_types

    arranges_exucutors = ArrayField(BigIntegerField(), default=list, null=True, blank=True)
    child_launches = ArrayField(BigIntegerField(), default=list, null=True, blank=True)
    childs = ArrayField(BigIntegerField(), default=list, null=True, blank=True)
    cnt_opers = PositiveIntegerField(null=True, blank=True)
    color = ForeignKeyProtect(Standard_colors, related_name='Production_order_tmp_color', null=True, blank=True)
    creator = ForeignKeyProtect(User, related_name='Production_order_tmp_creator', null=True, blank=True)
    date = DateTimeField(default=None, null=True, blank=True)
    demand_codes_str = CodeField(null=True, blank=True)
    demand_ids = ArrayField(BigIntegerField(), default=list, null=True, blank=True)
    description = TextField(null=True, blank=True)
    edizm = ForeignKeyProtect(Ed_izm, related_name='Production_order_tmp_edizmr', null=True, blank=True)
    edizm_arr = ArrayField(CodeField(), default=list, null=True, blank=True)
    enabled = BooleanField(null=True, blank=True)
    exucutors = ArrayField(BigIntegerField(), default=list, null=True, blank=True)
    exucutors_old = ArrayField(BigIntegerField(), default=list, null=True, blank=True)
    has_color = BooleanField(null=True, blank=True)
    has_launched = BooleanField(null=True, blank=True)
    id_f = BigIntegerField(db_index=True)
    id_real = BigIntegerField(db_index=True)
    isDeleted = BooleanField(null=True, blank=True)
    isFolder = BooleanField(null=True, blank=True)
    item = ForeignKeyProtect(Item, related_name='Production_order_tmp_item', null=True, blank=True)
    last_tech_operation = ForeignKeyProtect(Operations, null=True, blank=True)
    launch = ForeignKeyCascade(Launches, related_name='Production_order_tmp_launch', null=True, blank=True)
    launch_incom = ForeignKeyCascade(Launches, related_name='Production_order_tmp_launch_incom', null=True, blank=True)
    launches_odd = JSONFieldIVC(TextField(), null=True, blank=True)
    level = SmallIntegerField(null=True, blank=True)
    location = ForeignKeyProtect(Locations, related_name='Production_order_tmp_locations', null=True, blank=True)
    location_ids = ArrayField(BigIntegerField(), default=list, null=True, blank=True)
    location_ids_old = ArrayField(BigIntegerField(), default=list, null=True, blank=True)
    location_sector_ids = ArrayField(BigIntegerField(), default=list, null=True, blank=True)
    location_sectors_full_name = ArrayField(TextField(), default=list, null=True, blank=True)
    location_status_colors = JSONFieldIVC(null=True, blank=True)
    location_status_ids = JSONFieldIVC(null=True, blank=True)
    location_statuses = JSONFieldIVC(null=True, blank=True)
    location_values_made = JSONFieldIVC(null=True, blank=True)
    locations_sector_full_name = JSONFieldIVC(null=True, blank=True)
    location_sectors_ready = JSONFieldIVC(null=True, blank=True)
    num = CodeField(null=True, blank=True)
    opertype = ForeignKeyProtect(Operation_types, related_name='Production_order_tmp_opertype')
    parent_id = BigIntegerField(null=True, blank=True)
    parent_item = ForeignKeyProtect(Item, null=True, blank=True, related_name='Production_order_tmp_parent_item')
    parent_item_ids = ArrayField(BigIntegerField(), default=list, null=True, blank=True)
    parent_mul = SmallIntegerField(null=True, blank=True)
    process = BigIntegerField(default=None, db_index=True)
    props = Production_order_tmpManager.props()
    resource = ForeignKeyProtect(Resource, related_name='Production_order_tmp_resource', null=True, blank=True)
    status = ForeignKeyProtect(Status_operation_types)
    value1_sum = ArrayField(DecimalField(decimal_places=4, max_digits=19), null=True, blank=True)
    value_made = DecimalField(verbose_name='Количество  Выпущено', decimal_places=4, max_digits=19, null=True, blank=True)
    value_made_old = DecimalField(verbose_name='Количество  Выпущено', decimal_places=4, max_digits=19, null=True, blank=True)
    value_odd = DecimalField(verbose_name='Количество  Выпущено', decimal_places=4, max_digits=19, null=True, blank=True)
    value_start = DecimalField(verbose_name='Количество Запущено', decimal_places=4, max_digits=19, null=True, blank=True)
    value_sum = DecimalField(verbose_name='Количество по документации', decimal_places=4, max_digits=19, null=True, blank=True)

    objects = Production_order_tmpManager()
    tree_objects = TreeAuditModelManager()

    # started = Status_operation_types.objects.get(code='started')

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
        verbose_name = 'Временная таблица для выполнений пл Заказам на производство'
