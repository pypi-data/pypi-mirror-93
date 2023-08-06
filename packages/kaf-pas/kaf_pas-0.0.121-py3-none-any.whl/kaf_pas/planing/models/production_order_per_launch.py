import logging

from django.contrib.postgres.fields import ArrayField
from django.db.models import DecimalField, BigIntegerField, TextField, BooleanField, DateTimeField, PositiveIntegerField, SmallIntegerField

from isc_common.auth.models.user import User
from isc_common.datetime import DateTimeToStr
from isc_common.fields.code_field import CodeField, JSONFieldIVC
from isc_common.fields.related import ForeignKeyProtect, ForeignKeyCascade
from isc_common.managers.common_manager import CommonManager
from isc_common.models.audit import AuditModel
from isc_common.models.tree_audit import TreeAuditModelManager
from kaf_pas.ckk.models.item import Item
from kaf_pas.planing.models.operation_types import Operation_types
from kaf_pas.planing.models.production_order import Production_orderQuerySet
from kaf_pas.planing.operation_typesStack import DETAIL_OPERS_PRD_TSK
from kaf_pas.production.models.launches import Launches

logger = logging.getLogger(__name__)


class Production_order_per_launchManager(CommonManager):

    def get_queryset(self):
        return Production_orderQuerySet(self.model, using=self._db)


class Production_order_per_launch(AuditModel):
    from kaf_pas.planing.models.status_operation_types import Status_operation_types
    from kaf_pas.planing.models.operation_refs import Operation_refsManager

    arranges_exucutors = ArrayField(BigIntegerField(), default=list)
    child_launches = ArrayField(BigIntegerField(), default=list)
    cnt_opers = PositiveIntegerField()
    creator = ForeignKeyProtect(User, related_name='Production_order_per_launch_creator')
    date = DateTimeField(default=None)
    demand_codes_str = CodeField()
    demand_ids = ArrayField(BigIntegerField(), default=list)
    description = TextField(null=True, blank=True)
    edizm_arr = ArrayField(CodeField(null=True, blank=True))
    exucutors = ArrayField(BigIntegerField(), default=list)
    exucutors_old = ArrayField(BigIntegerField(), default=list)
    id_f = BigIntegerField()
    isDeleted = BooleanField()
    isFolder = BooleanField(default=None)
    item = ForeignKeyProtect(Item, related_name='Production_order_per_launch_item')
    launch = ForeignKeyCascade(Launches)
    location_ids = ArrayField(BigIntegerField(), default=list)
    location_ids_old = ArrayField(BigIntegerField(), default=list)
    location_sector_ids = ArrayField(BigIntegerField(), default=list)
    location_sectors_full_name = ArrayField(TextField(), default=list)
    location_status_colors = JSONFieldIVC()
    location_status_ids = JSONFieldIVC()
    location_values_made = JSONFieldIVC()
    location_sectors_ready = JSONFieldIVC()
    location_statuses = JSONFieldIVC()
    locations_sector_full_name = JSONFieldIVC()
    max_level = SmallIntegerField()
    num = CodeField()
    opertype = ForeignKeyProtect(Operation_types, related_name='Production_order_per_launch_opertype')
    parent_id = BigIntegerField(null=True, blank=True)
    parent_item = ForeignKeyProtect(Item, null=True, blank=True, related_name='Production_order_per_launch_parent_item')
    parent_item_ids = ArrayField(BigIntegerField(), default=list)
    props = Operation_refsManager.props()
    status = ForeignKeyProtect(Status_operation_types)
    value1_sum = DecimalField(decimal_places=4, max_digits=19)
    value_made = DecimalField(decimal_places=4, max_digits=19, null=True, blank=True)
    value_odd = DecimalField(decimal_places=4, max_digits=19)
    value_start = DecimalField(decimal_places=4, max_digits=19, null=True, blank=True)
    value_sum = DecimalField(decimal_places=4, max_digits=19)

    objects = Production_order_per_launchManager()
    tree_objects = TreeAuditModelManager()

    @classmethod
    def all_childs(cls, id):
        from kaf_pas.planing.models.production_order_opers_per_launch import Production_order_opers_per_launch
        return Production_order_opers_per_launch.objects.filter(parent_id=id, opertype__code=DETAIL_OPERS_PRD_TSK).alive().order_by('production_operation_num')

    def __str__(self):
        return f'\nid: {self.id}, ' \
               f'\nid_f: {self.id_f}, ' \
               f'\nparent_id: {self.parent_id}, ' \
               f'\ndate: {DateTimeToStr(self.date)}, ' \
               f'\nnum: {self.num}, ' \
               f'\ndescription: {self.description}, ' \
               f'\nopertype: [{self.opertype}], ' \
               f'\ncreator: [{self.creator}], ' \
               f'\nexucutors: [{self.exucutors}], ' \
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
               f'\nvalue_odd: {self.value_odd}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Заказы на производство'
        managed = False
        # db_table = 'planing_production_order_per_launch_view'
        db_table = 'planing_production_order_per_launch_tbl'
