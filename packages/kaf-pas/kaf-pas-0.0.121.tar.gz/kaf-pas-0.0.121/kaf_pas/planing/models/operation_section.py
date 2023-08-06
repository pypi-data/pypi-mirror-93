import logging

from bitfield import BitField

from isc_common.fields.related import ForeignKeyCascade
from isc_common.models.audit import AuditModel, AuditManager
from kaf_pas.planing.models.operations import Operations, BaseOperationQuerySet
from kaf_pas.planing.models.sections import Sections

logger = logging.getLogger(__name__)


class Operation_sectionQuerySet(BaseOperationQuerySet):
    pass


class Operation_sectionManager(AuditManager):

    @classmethod
    def props(cls):
        return BitField(flags=(
            ('isProductionOrder', 'Уровень заказа на производство'),  # 1
        ), default=0, db_index=True)

    @classmethod
    def getRecord(cls, record):
        res = {
            'id': record.id,
            'editing': record.editing,
            'deliting': record.deliting,
        }
        return res

    def get_queryset(self):
        return Operation_sectionQuerySet(self.model, using=self._db)


class Operation_section(AuditModel):
    operation = ForeignKeyCascade(Operations)
    section = ForeignKeyCascade(Sections)

    objects = Operation_sectionManager()

    def __str__(self):
        return f"ID:{self.id}, section: [{self.section}] , operation: [{self.operation}]"

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Кросс-таблица'
        unique_together = (('operation', 'section'),)
