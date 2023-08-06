import logging

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db.models import DecimalField, DateTimeField, TextField, BooleanField, BigIntegerField, SmallIntegerField

from isc_common.auth.models.user import User
from isc_common.datetime import DateTimeToStr
from isc_common.fields.code_field import CodeField
from isc_common.fields.name_field import NameField
from isc_common.fields.related import ForeignKeyProtect
from isc_common.managers.common_manager import CommonManager
from isc_common.models.audit import AuditQuerySet, AuditModel
from isc_common.models.tree_audit import TreeAuditModelManager
from isc_common.number import DecimalToStr
from isc_common.ws.webSocket import WebSocket

logger = logging.getLogger(__name__)


class Production_order_made_historyQuerySet(AuditQuerySet):
    pass


class Production_order_made_historyManager(CommonManager):
    def get_queryset(self):
        return Production_order_made_historyQuerySet(self.model, using=self._db)

    @classmethod
    def getRecord(cls, record):
        res = {
            'color__color__color': record.color_color,
            'color_color_name': record.color_name,
            'creator_short_name': record.creator_short_name,
            'date': record.date,
            'demand_codes_str': record.demand_codes_str,
            'description': record.description,
            'edizm_name': record.edizm_name,
            'id': record.id,
            'id_f': record.id_f,
            'id_real': record.id_real,
            'isFolder': record.isFolder if record.isFolder is not None else False,
            'item_STMP_1__value_str': record.item_STMP_1_value_str,
            'item_STMP_2__value_str': record.item_STMP_2_value_str,
            'launch_code': record.launch_code,
            'launch_date': record.launch_date,
            'launch_incom_code': record.launch_incom_code,
            'launch_incom_date': record.launch_incom_date,
            'level': record.level,
            'location_sectors_full_name': record.location_sectors_full_name,
            'parent_id': record.parent_id,
            'props': record.props,
            'status_code': record.status_code,
            'status_name': record.status_name,
            'value1_sum': DecimalToStr(record.value1_sum, noneId_0=True),
            'value_made': DecimalToStr(record.value_made, noneId_0=True),
            'value_odd': DecimalToStr(record.value_odd, noneId_0=True),
            'value_start': DecimalToStr(record.value_start),
            'value_sum': DecimalToStr(record.value_sum),
        }
        return res

    @classmethod
    def fullRows(cls, suffix=''):
        WebSocket.full_refresh_grid(grid_id=f'{settings.GRID_CONSTANTS.refresh_ProductionOrderMadeHistory_grid}{suffix}')


class Production_order_made_history(AuditModel):
    from kaf_pas.planing.models.operation_refs import Operation_refsManager

    color_color = CodeField(null=True, blank=True)
    color_name = CodeField(null=True, blank=True)
    create_date = DateTimeField(db_index=True)
    creator_short_name = CodeField(null=True, blank=True)
    date = DateTimeField(null=True, blank=True)
    demand_codes_str = CodeField(null=True, blank=True)
    description = TextField(null=True, blank=True)
    edizm_name = NameField(null=True, blank=True)
    edizm_arr = ArrayField(CodeField(), default=list, null=True, blank=True)
    executor = ForeignKeyProtect(User, related_name='Production_order_made_history_executor')
    id_f = BigIntegerField(db_index=True)
    id_real = BigIntegerField(db_index=True)
    isFolder = BooleanField(null=True, blank=True)
    item_STMP_1_value_str = NameField(null=True, blank=True)
    item_STMP_2_value_str = NameField(null=True, blank=True)
    launch_code = CodeField(null=True, blank=True)
    launch_date = DateTimeField(null=True, blank=True)
    launch_incom_code = CodeField(null=True, blank=True)
    launch_incom_date = DateTimeField(null=True, blank=True)
    level = SmallIntegerField(null=True, blank=True)
    location_sectors_full_name = TextField(null=True, blank=True)
    parent_id = BigIntegerField(null=True, blank=True)
    process = BigIntegerField(db_index=True)
    props = Operation_refsManager.props()
    status_code = CodeField(null=True, blank=True)
    status_name = NameField(null=True, blank=True)
    value1_sum = CodeField(null=True, blank=True)
    value_made = DecimalField(verbose_name='Количество  Выпущено', decimal_places=4, max_digits=19, null=True, blank=True)
    value_odd = DecimalField(verbose_name='Количество  Выпущено', decimal_places=4, max_digits=19, null=True, blank=True)
    value_start = DecimalField(verbose_name='Количество Запущено', decimal_places=4, max_digits=19, null=True, blank=True)
    value_sum = DecimalField(verbose_name='Количество по документации', decimal_places=4, max_digits=19, null=True, blank=True)

    objects = Production_order_made_historyManager()
    tree_objects = TreeAuditModelManager()

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
        verbose_name = 'Выполнения по Заказам на производство'
