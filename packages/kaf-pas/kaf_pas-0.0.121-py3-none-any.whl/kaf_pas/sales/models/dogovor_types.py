import logging

from bitfield import BitField

from isc_common.models.base_ref import BaseRef, BaseRefManager, BaseRefQuerySet

logger = logging.getLogger(__name__)


class Dogovor_typesQuerySet(BaseRefQuerySet):
    pass


class Dogovor_typesManager(BaseRefManager):

    @classmethod
    def getRecord(cls, record):
        res = {
            'id': record.id,
            'code': record.code,
            'name': record.name,
            'description': record.description,

            'editing': record.editing,
            'deliting': record.deliting,
        }
        return res

    def get_queryset(self):
        return Dogovor_typesQuerySet(self.model, using=self._db)


class Dogovor_types(BaseRef):
    props = BitField(flags=(
        ('real', 'Реальный тим'),
    ), default=1, db_index=True)

    objects = Dogovor_typesManager()

    def __str__(self):
        return f"ID:{self.id}, code: {self.code}, name: {self.name}, description: {self.description}"

    class Meta:
        verbose_name = 'Типы договорных документов'
