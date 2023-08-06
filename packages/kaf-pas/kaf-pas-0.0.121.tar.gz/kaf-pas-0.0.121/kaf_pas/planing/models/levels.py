import logging

from django.db.models import PositiveIntegerField

from isc_common.models.base_ref import BaseRef, BaseRefManager, BaseRefQuerySet

logger = logging.getLogger(__name__)


class LevelsQuerySet(BaseRefQuerySet):
    pass


class LevelsManager(BaseRefManager):

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
        return LevelsQuerySet(self.model, using=self._db)


class Levels(BaseRef):
    code = PositiveIntegerField(db_index=True, unique=True)
    objects = LevelsManager()

    def __str__(self):
        return f'ID:{self.id}, code: {self.code}, name: {self.name}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Уровни производственного цикла'
