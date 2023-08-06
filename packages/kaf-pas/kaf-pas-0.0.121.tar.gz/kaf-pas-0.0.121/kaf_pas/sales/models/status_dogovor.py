import logging

from bitfield import BitField

from isc_common.bit import IsBitOn
from isc_common.models.base_ref import BaseRef, BaseRefQuerySet, StatusBaseRefManager

logger = logging.getLogger(__name__)


class StatusDogovorQuerySet(BaseRefQuerySet):
    pass


class StatusDogovorManager(StatusBaseRefManager):

    @classmethod
    def getRecord(cls, record):
        res = {
            'id': record.id,
            'code': record.code,
            'name': record.name,
            'description': record.description,
            'props': record.props._value,
            'disabled': IsBitOn(record.props, 1),
            'editing': record.editing,
            'deliting': record.deliting,
        }
        return res

    def get_queryset(self):
        return StatusDogovorQuerySet(self.model, using=self._db)


class StatusDogovor(BaseRef):
    props = BitField(flags=(
        ('disabled', 'Неактивная запись в гриде')
    ), default=1, db_index=True)
    objects = StatusDogovorManager()

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = 'Статусы договоров'
