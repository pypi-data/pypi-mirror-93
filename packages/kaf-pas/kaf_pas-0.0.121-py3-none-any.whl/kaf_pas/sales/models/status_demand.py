import logging

from bitfield import BitField

from isc_common.bit import IsBitOn
from isc_common.models.base_ref import BaseRef, BaseRefQuerySet, StatusBaseRefManager

logger = logging.getLogger(__name__)


class Status_demandQuerySet(BaseRefQuerySet):
    pass


class Status_demandManager(StatusBaseRefManager):

    @classmethod
    def getRecord(cls, record):
        res = {
            'id': record.id,
            'code': record.code,
            'name': record.name,
            'description': record.description,
            'props': record.props._value,
            'disabled': IsBitOn(record.props, 0),
            'editing': record.editing,
            'deliting': record.deliting,
        }
        return res

    def get_queryset(self):
        return Status_demandQuerySet(self.model, using=self._db)


class Status_demand(BaseRef):
    props = BitField(flags=(
        ('disabled', 'Неактивная запись в гриде')
    ), default=0, db_index=True)

    objects = Status_demandManager()

    def __str__(self):
        return f"ID:{self.id}, code: {self.code}, name: {self.name}, description: {self.description}"

    class Meta:
        verbose_name = 'Статусы заказов на продажу'
