import logging

from bitfield import BitField
from django.db import transaction
from django.db.models import TextField

from clndr.models.calendars import Calendars
from isc_common import delAttr, setAttr
from isc_common.common import notDefined
from isc_common.common.functions import ExecuteStoredProc
from isc_common.fields.code_field import CodeField, CodeStrictField
from isc_common.fields.related import ForeignKeyProtect
from isc_common.http.DSRequest import DSRequest
from isc_common.managers.common_managet_with_lookup_fields import CommonManagetWithLookUpFieldsManager, CommonManagetWithLookUpFieldsQuerySet
from isc_common.models.base_ref import BaseRefHierarcy, BaseRefQuerySet
from isc_common.models.tree_audit import TreeAuditModelManager
from isc_common.number import DelProps, model_2_dict

logger = logging.getLogger(__name__)


class LocationsQuerySet(BaseRefQuerySet, CommonManagetWithLookUpFieldsQuerySet):
    pass


class LocationsManager(CommonManagetWithLookUpFieldsManager):
    def createFromRequest(self, request, propsArr):
        request = DSRequest(request=request)
        data = request.get_data()
        workshop = Locations.objects.get(code='00')

        _data = data.copy()

        delAttr(_data, 'id')
        setAttr(_data, 'workshop', workshop)
        setAttr(_data, 'fullname', '/')
        props = self.get_prp(data=_data, propsArr=propsArr)
        if props > -1:
            setAttr(_data, 'props', props)

        with transaction.atomic():
            res = super().create(**_data)

            workshop_id = ExecuteStoredProc('get_workshop_id', [res.id])
            res.workshop_id = workshop_id

            fullname = ExecuteStoredProc('get_full_name', [res.id, 'ckk_locations'])
            res.fullname = fullname

            res.save()

            data.update(DelProps(model_2_dict(res)))
            return data

    def updateFromRequest(self, request, removed=None, function=None, propsArr=None):
        if not isinstance(request, DSRequest):
            request = DSRequest(request=request)
        data = request.get_data()
        _data = data.copy()
        parent_id = data.get('parent_id')
        props = self.get_prp(data=_data, propsArr=propsArr)
        _data = self.delete_underscore_element(_data)

        delAttr(_data, 'id')
        delAttr(_data, 'full_name')
        delAttr(_data, 'calendar__full_name')
        delAttr(_data, 'grouping_production_orders')
        delAttr(_data, 'isWorkshop')
        delAttr(_data, 'isFolder')

        if props > -1:
            setAttr(_data, 'props', props)

        with transaction.atomic():
            workshop_id = ExecuteStoredProc('get_workshop_id', [data.get('id')])
            setAttr(_data, 'workshop_id', workshop_id)

            fullname = ExecuteStoredProc('get_full_name', [data.get('id'), 'ckk_locations'])
            setAttr(_data, 'fullname', fullname)
            setAttr(data, 'fullname', fullname)

            setAttr(_data, 'parent_id', parent_id)

            super().update_or_create(id=data.get('id'), defaults=_data)
            super().filter(id=data.get('id')).update(fullname=fullname)

            return data

    @classmethod
    def props(cls):
        return BitField(flags=(
            ('isWorkshop', 'Уровень цеха'),  # 1
            ('grouping_production_orders', 'Группировать задания на производство'),  # 2
        ), default=0, db_index=True)

    @classmethod
    def getRecord(cls, record):
        res = {
            'calendar__full_name': record.calendar.full_name if record.calendar else None,
            'calendar_id': record.calendar.id if record.calendar else None,
            'code': record.code,
            'color': record.color,
            'deliting': record.deliting,
            'description': record.description,
            'editing': record.editing,
            'full_name': record.fullname,
            'grouping_production_orders': record.props.grouping_production_orders,
            'id': record.id,
            'isWorkshop': record.props.isWorkshop,
            'name': record.name,
            'parent_id': record.parent.id if record.parent else None,
            'props': record.props,
        }
        return DelProps(res)

    def get_queryset(self):
        return LocationsQuerySet(self.model, using=self._db)


class Locations(BaseRefHierarcy):
    calendar = ForeignKeyProtect(Calendars, null=True, blank=True)
    code = CodeStrictField(unique=True)
    color = CodeField()
    fullname = TextField()
    props = LocationsManager.props()
    workshop = ForeignKeyProtect('self', related_name='Locations_workshop')

    objects = LocationsManager()

    objects_tree = TreeAuditModelManager()

    def _get_calendar(self, parent):
        if parent:
            if parent.calendar:
                return parent.calendar
            else:
                return self._get_calendar(parent=parent.parent)
        else:
            return None

    @property
    def is_workshop(self):
        return self.props.isWorkshop.is_set

    @property
    def is_grouping_production_orders(self):
        return self.props.grouping_production_orders.is_set

    @property
    def resource(self):
        from kaf_pas.production.models.resource import Resource
        resource, _ = Resource.objects.get_or_create(location_id=self.id, code='none', defaults=dict(name=notDefined))
        return resource

    @property
    def get_calendar(self):
        if self.calendar:
            return self.calendar

        return self._get_calendar(parent=self.parent)

    def __repr__(self):
        return self.full_name

    def __str__(self):
        return f"ID: {self.id}, code: {self.code}, name: {self.name}, full_name: {self.full_name}, description: {self.description}"

    class Meta:
        verbose_name = 'Место положения'
