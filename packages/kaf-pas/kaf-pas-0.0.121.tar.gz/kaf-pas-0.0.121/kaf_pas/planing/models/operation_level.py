import logging

from bitfield import BitField

from isc_common.fields.related import ForeignKeyCascade
from isc_common.models.audit import AuditModel, AuditManager
from kaf_pas.planing.models.levels import Levels
from kaf_pas.planing.models.operations import Operations, BaseOperationQuerySet

logger = logging.getLogger(__name__)


class Operation_levelQuerySet(BaseOperationQuerySet):
    pass


class Operation_levelManager(AuditManager):

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
        return Operation_levelQuerySet(self.model, using=self._db)


class Operation_level(AuditModel):
    operation = ForeignKeyCascade(Operations, related_name='planing_operation_1')
    level = ForeignKeyCascade(Levels, related_name='planing_lev_1')
    props = Operation_levelManager.props()

    objects = Operation_levelManager()

    def __str__(self):
        return f"ID:{self.id}, level: [{self.level}] , operation: [{self.operation}]"

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Кросс-таблица'
        unique_together = (('operation', 'level'),)
