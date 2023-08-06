import logging

from django.db.models import PositiveIntegerField, DateTimeField, BooleanField, DecimalField

from isc_common.bit import IsBitOff
from isc_common.fields.code_field import CodeField
from isc_common.fields.related import ForeignKeyProtect, ForeignKeyCascade
from isc_common.managers.common_managet_with_lookup_fields import CommonManagetWithLookUpFieldsManager, CommonManagetWithLookUpFieldsQuerySet
from isc_common.models.base_ref import BaseRefHierarcy
from isc_common.number import ToDecimal, ToStr, ToInt
from kaf_pas.kd.models.document_attributes import Document_attributes
from kaf_pas.sales.models.precent import Precent
from kaf_pas.sales.models.precent_dogovors import Precent_dogovors
from kaf_pas.sales.models.precent_items import Precent_items
from kaf_pas.sales.models.status_demand import Status_demand

logger = logging.getLogger(__name__)


class Demand_viewQuerySet(CommonManagetWithLookUpFieldsQuerySet):
    pass


class Demand_viewManager(CommonManagetWithLookUpFieldsManager):

    @classmethod
    def getRecord(cls, record):
        res = {
            'code': record.code,
            'date': record.date,
            'date_sign': record.precent.date_sign,
            'deliting': record.deliting,
            'description': record.description,
            'editing': record.editing,
            'enabled': IsBitOff(record.status.props, 0),
            'id': record.id,
            'isFolder': record.isFolder,
            'launch_qty': ToInt(record.launch_qty),
            'name': record.name,
            'parent': record.parent.id if record.parent else None,
            'parent_id': record.parent.id if record.parent else None,
            'precent__code': record.precent.code,
            'precent__date': record.precent.date,
            'precent__precent_type__name': record.precent.precent_type.name,
            'precent__precent_type_id': record.precent.precent_type.id,
            'precent_dogovor__code': record.precent_dogovor.dogovor.code,
            'precent_dogovor__date': record.precent_dogovor.dogovor.date,
            'precent_dogovor__dogovor__customer__name': record.precent_dogovor.dogovor.customer.name,
            'precent_dogovor__name': record.precent_dogovor.dogovor.name,
            'precent_dogovor_id': record.precent_dogovor.id,
            'precent_id': record.precent.id,
            'precent_item__STMP_1__value_str': record.precent_item.item.STMP_1.value_str if record.precent_item.item.STMP_1 else None,
            'precent_item__STMP_1_id': record.precent_item.item.STMP_1.id if record.precent_item.item.STMP_1 else None,
            'precent_item__STMP_2__value_str': record.precent_item.item.STMP_2.value_str if record.precent_item.item.STMP_2 else None,
            'precent_item__STMP_2_id': record.precent_item.item.STMP_2.id if record.precent_item.item.STMP_2 else None,
            'precent_item_id': record.precent_item.id,
            'qty': record.qty,
            'qty_for_launch': ToInt(record.qty_for_launch),
            'status__code': record.status.code,
            'status__name': record.status.name,
            'status_id': record.status.id,
            'tail_qty': ToInt(record.tail_qty),
        }
        return res

    @classmethod
    def getRecord1(cls, record):
        enabled = record.tail_qty > 0

        res = {
            'code': record.code,
            'date': record.date,
            'date_sign': record.precent.date_sign,
            'deliting': record.deliting,
            'description': record.description,
            'editing': record.editing,
            'enabled' : enabled,
            'id': record.id,
            'isFolder': record.isFolder,
            'launch_qty': ToInt(record.launch_qty),
            'name': record.name,
            'parent': record.parent.id if record.parent else None,
            'parent_id': record.parent.id if record.parent else None,
            'precent__code': record.precent.code,
            'precent__date': record.precent.date,
            'precent__precent_type__name': record.precent.precent_type.name,
            'precent__precent_type_id': record.precent.precent_type.id,
            'precent_dogovor__code': record.precent_dogovor.dogovor.code,
            'precent_dogovor__date': record.precent_dogovor.dogovor.date,
            'precent_dogovor__dogovor__customer__name': record.precent_dogovor.dogovor.customer.name,
            'precent_dogovor__name': record.precent_dogovor.dogovor.name,
            'precent_dogovor_id': record.precent_dogovor.id,
            'precent_id': record.precent.id,
            'precent_item__STMP_1__value_str': record.precent_item.item.STMP_1.value_str if record.precent_item.item.STMP_1 else None,
            'precent_item__STMP_1_id': record.precent_item.item.STMP_1.id if record.precent_item.item.STMP_1 else None,
            'precent_item__STMP_2__value_str': record.precent_item.item.STMP_2.value_str if record.precent_item.item.STMP_2 else None,
            'precent_item__STMP_2_id': record.precent_item.item.STMP_2.id if record.precent_item.item.STMP_2 else None,
            'precent_item_id': record.precent_item.id,
            'qty': record.qty,
            'qty_for_launch': ToInt(record.qty_for_launch),
            'status__code': record.status.code,
            'status__name': record.status.name,
            'status_id': record.status.id,
            'tail_qty': ToInt(record.tail_qty),
        }
        return res

    def get_queryset(self):
        return Demand_viewQuerySet(self.model, using=self._db)


class Demand_view(BaseRefHierarcy):
    date = DateTimeField()
    isFolder = BooleanField()
    launch_qty = PositiveIntegerField()
    precent = ForeignKeyCascade(Precent)
    precent_dogovor = ForeignKeyCascade(Precent_dogovors)
    precent_item = ForeignKeyCascade(Precent_items)
    qty = PositiveIntegerField()
    qty_for_launch = PositiveIntegerField(null=True, blank=True)
    status = ForeignKeyProtect(Status_demand)
    tail_qty = PositiveIntegerField()
    STMP_1 = ForeignKeyProtect(Document_attributes, related_name='Demand_view_STMP_1', null=True, blank=True)
    STMP_2 = ForeignKeyProtect(Document_attributes, related_name='Demand_view_STMP_2', null=True, blank=True)

    objects = Demand_viewManager()

    def __str__(self):
        return f"ID:{self.id}, code: {self.code}, name: {self.name}, description: {self.description}"

    @property
    def year_month(self):
        return f'{self.year} / {self.month}'

    class Meta:
        verbose_name = 'Заказы на продажу'
        db_table = 'sales_demand_view'
        managed = False
