import logging

from isc_common.fields.related import ForeignKeyProtect, ForeignKeyCascade
from isc_common.models.audit import AuditModel, AuditManager, AuditQuerySet
from kaf_pas.planing.models.operations import Operations
from kaf_pas.planing.models.production_order_made_history import Production_order_made_history

logger = logging.getLogger(__name__)


class Production_order_made_history_operationsQuerySet(AuditQuerySet):
    pass


class Production_order_made_history_operationsManager(AuditManager):

    @classmethod
    def getRecord(cls, record):
        res = {
            'id': record.id,
            'editing': record.editing,
            'deliting': record.deliting,
        }
        return res

    def get_queryset(self):
        return Production_order_made_history_operationsQuerySet(self.model, using=self._db)


class Production_order_made_history_operations(AuditModel):
    production_order_made_history = ForeignKeyProtect(Production_order_made_history)
    operation = ForeignKeyCascade(Operations)

    objects = Production_order_made_history_operationsManager()

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Кросс таблица'
