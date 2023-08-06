import logging

from bitfield import BitField
from django.db.models import PositiveIntegerField

from isc_common.fields.related import ForeignKeyCascade
from isc_common.models.audit import AuditModel, AuditManager, AuditQuerySet
from kaf_pas.ckk.models.item import Item

logger = logging.getLogger(__name__)


class Item_qtyQuerySet(AuditQuerySet):
    def create(self, **kwargs):
        return super().create(**kwargs)

    def filter(self, *args, **kwargs):
        return super().filter(*args, **kwargs)


class Item_qtyManager(AuditManager):

    @classmethod
    def get_prop(cls):
        return BitField(flags=(
            ('items', 'Состав изделия (Технологическая спецификация)'),  # 1
            ('teach', 'Производственная спецификация'),  # 2
        ), default=1, db_index=True)

    @classmethod
    def getRecord(cls, record):
        res = {
            'id': record.id,
            'editing': record.editing,
            'deliting': record.deliting,
        }
        return res

    def get_queryset(self):
        return Item_qtyQuerySet(self.model, using=self._db)


class Item_qty(AuditModel):
    child = ForeignKeyCascade(Item, related_name='Item_qty_child')
    parent = ForeignKeyCascade(Item, related_name='Item_qty_parent', blank=True, null=True)
    qty = PositiveIntegerField()
    props = Item_qtyManager.get_prop()

    objects = Item_qtyManager()

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Количество элементов'
