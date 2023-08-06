import logging

from django.db.models import BooleanField

from clndr.models.calendars import Calendars
from isc_common.fields.related import ForeignKeyProtect
from isc_common.managers.common_managet_with_lookup_fields import CommonManagetWithLookUpFieldsQuerySet, CommonManagetWithLookUpFieldsManager
from isc_common.models.base_ref import BaseRef
from isc_common.number import DelProps
from kaf_pas.ckk.models.locations import Locations

logger = logging.getLogger(__name__)


class Resource_viewQuerySet(CommonManagetWithLookUpFieldsQuerySet):
    def filter(self, *args, **kwargs):
        return super().filter(*args, **kwargs)


class Resource_viewManager(CommonManagetWithLookUpFieldsManager):

    @classmethod
    def getRecord(cls, record):
        res = {
            'id': record.id,
            'code': record.code,
            'name': record.name,
            'description': record.description,
            'isFolder': record.isFolder,
            'calendar_id': record.calendar.id if record.calendar else None,
            'calendar__full_name': record.calendar.full_name if record.calendar else None,
            # 'isWorkshop': record.props.isWorkshop,
            # 'props': record.props,
            'editing': record.editing,
            'deliting': record.deliting,
        }
        return DelProps(res)

    def get_queryset(self):
        return Resource_viewQuerySet(self.model, using=self._db)

    @property
    def full_name(self):
        return f'{self.location.full_name}/{super().full_name}'


class Resource_view(BaseRef):
    location = ForeignKeyProtect(Locations, related_name='Resource_view_location')
    location_fin = ForeignKeyProtect(Locations, null=True, blank=True, related_name='Resource_view_location_fin')
    calendar = ForeignKeyProtect(Calendars, null=True, blank=True)
    isFolder = BooleanField()
    # props = ResourceManager.props()

    objects = Resource_viewManager()

    def __str__(self):
        return f"{self.id}"

    class Meta:
        db_table = 'production_resource_view'
        managed = False
        verbose_name = 'Ресурсы'
