import logging

from django.db.models import PositiveIntegerField

from isc_common.fields.related import ForeignKeyProtect, ForeignKeyCascade
from isc_common.managers.common_managet_with_lookup_fields import CommonManagetWithLookUpFieldsQuerySet, CommonManagetWithLookUpFieldsManager
from isc_common.models.audit import AuditModel
from kaf_pas.ckk.models.item import Item
from kaf_pas.sales.models.precent_dogovors import Precent_dogovors

logger = logging.getLogger(__name__)


class Precent_itemsQuerySet(CommonManagetWithLookUpFieldsQuerySet):
    def filter(self, *args, **kwargs):
        return super().filter(*args, **kwargs)


class Precent_itemsManager(CommonManagetWithLookUpFieldsManager):

    @classmethod
    def getRecord(cls, record):
        res = {
            'id': record.id,
            'item_id': record.item.id,
            'item__STMP_1_id': record.item.STMP_1.id if record.item.STMP_1 else None,
            'item__STMP_1__value_str': record.item.STMP_1.value_str if record.item.STMP_1 else None,
            'item__STMP_2_id': record.item.STMP_2.id if record.item.STMP_2 else None,
            'item__STMP_2__value_str': record.item.STMP_2.value_str if record.item.STMP_2 else None,
            'precent_dogovor_id': record.precent_dogovor.id,
            'qty': record.qty,
            'lastmodified': record.lastmodified,
            'editing': record.editing,
            'deliting': record.deliting,
        }
        return res

    def get_queryset(self):
        return Precent_itemsQuerySet(self.model, using=self._db)


class Precent_items(AuditModel):
    item = ForeignKeyProtect(Item)
    precent_dogovor = ForeignKeyCascade(Precent_dogovors)
    qty = PositiveIntegerField(null=True, blank=True)

    objects = Precent_itemsManager()

    def __str__(self):
        return f'{self.id}, qty: {self.qty}, item: [{self.item}], precent_dogovor: [{self.precent_dogovor}]'

    class Meta:
        verbose_name = 'Комплектация распоряжения'
        # unique_together = (('item', 'precent'),)
