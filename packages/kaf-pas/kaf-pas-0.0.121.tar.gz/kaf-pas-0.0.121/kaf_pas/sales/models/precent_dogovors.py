import logging

from isc_common.fields.related import ForeignKeyCascade
from isc_common.managers.common_managet_with_lookup_fields import CommonManagetWithLookUpFieldsQuerySet, CommonManagetWithLookUpFieldsManager
from isc_common.models.audit import AuditModel
from kaf_pas.sales.models.dogovors import Dogovors
from kaf_pas.sales.models.precent import Precent

logger = logging.getLogger(__name__)


class Precent_dogovorsQuerySet(CommonManagetWithLookUpFieldsQuerySet):
    pass


class Precent_dogovorsManager(CommonManagetWithLookUpFieldsManager):

    @classmethod
    def getRecord(cls, record):
        res = {
            'id': record.id,
            'dogovor_id': record.dogovor.id,
            'dogovor__name': record.dogovor.name,
            'dogovor__full_name': record.dogovor.full_name,
            'dogovor__date': record.dogovor.date,
            'dogovor__customer_id': record.dogovor.customer.id,
            'dogovor__customer__name': record.dogovor.customer.name,
            'editing': record.editing,
            'deliting': record.deliting,
            # 'enabled': IsBitOn(record.dogovor.props, 0)
        }
        return res

    def get_queryset(self):
        return Precent_dogovorsQuerySet(self.model, using=self._db)


class Precent_dogovors(AuditModel):
    dogovor = ForeignKeyCascade(Dogovors)
    precent = ForeignKeyCascade(Precent)

    objects = Precent_dogovorsManager()

    def __str__(self):
        return f"ID:{self.id}, dogovor: [{self.dogovor}], precent: {self.precent}"

    class Meta:
        verbose_name = 'Кросс-таблица'
