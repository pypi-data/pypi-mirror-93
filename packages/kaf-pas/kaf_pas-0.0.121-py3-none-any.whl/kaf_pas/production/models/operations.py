import logging

from bitfield import BitField
from django.db.models import TextField

from isc_common import setAttr, delAttr
from isc_common.bit import IsBitOn
from isc_common.common.functions import ExecuteStoredProc
from isc_common.fields.code_field import CodeStrictField
from isc_common.fields.name_field import NameStrictField
from isc_common.http.DSRequest import DSRequest
from isc_common.managers.common_managet_with_lookup_fields import CommonManagetWithLookUpFieldsManager, CommonManagetWithLookUpFieldsQuerySet
from isc_common.models.base_ref import BaseRefHierarcy, BaseRefQuerySet
from isc_common.number import DelProps, model_2_dict

logger = logging.getLogger(__name__)


class OperationsQuerySet(BaseRefQuerySet, CommonManagetWithLookUpFieldsQuerySet):
    pass


class OperationsManager(CommonManagetWithLookUpFieldsManager):

    def createFromRequest(self, request, removed=None, propsArr=None):
        request = DSRequest(request=request)
        data = request.get_data()
        _data = data.copy()

        self._remove_prop(_data, removed)

        props = self.get_prp(data=_data, propsArr=propsArr)
        if props > -1:
            setAttr(_data, 'props', props)

        delAttr(_data, 'id')
        setAttr(_data, 'fullname', '/')
        res = super().create(**_data)

        fullname = ExecuteStoredProc('get_full_name', [res.id, 'production_operations'])
        res.fullname = fullname

        res.save()

        setAttr(res, 'fullname', fullname)
        data.update(DelProps(model_2_dict(res)))
        return data

    def updateFromRequest(self, request, removed=None, function=None, propsArr=None):
        if not isinstance(request, DSRequest):
            request = DSRequest(request=request)
        data = request.get_data()

        _data = data.copy()
        delAttr(_data, 'id')
        delAttr(_data, 'full_name')
        delAttr(_data, 'full_name_real')
        delAttr(_data, 'absorption')
        delAttr(_data, 'isFolder')
        delAttr(_data, 'launched')
        delAttr(_data, 'grouped')
        delAttr(_data, 'transportation')

        id = data.get('id')

        self._remove_prop(data, removed)
        data = self._remove_prop_(data)
        props = self.get_prp(data=data, propsArr=propsArr)
        if props > -1:
            setAttr(_data, 'props', props)

        fullname = ExecuteStoredProc('get_full_name', [id, 'production_operations'])
        setAttr(data, 'fullname', fullname)

        super().update_or_create(id=id, defaults=_data)
        return data

    @classmethod
    def getRecord(cls, record):
        res = {
            'absorption': record.props.absorption,
            'code': record.code,
            'deliting': record.deliting,
            'description': record.description,
            'editing': record.editing,
            'full_name': record.fullname,
            'id': record.id,
            'lastmodified': record.lastmodified,
            'launched': record.props.launched,
            'name': record.name,
            'parent_id': record.parent_id,
            # 'partition_to_launch': record.props.partition_to_launch,
            'props': record.props,
            'transportation': record.props.transportation,
        }
        return DelProps(res)

    def get_queryset(self):
        return OperationsQuerySet(self.model, using=self._db)

    @classmethod
    def get_props(cls):
        return BitField(flags=(
            ('launched', 'Возможность привязки к запуску'),  # 0
            ('grouped', 'Группировка'),  # 1
            ('transportation', 'Операция транспортировки'),  # 2
            ('absorption', 'Операция поглощения'),  # 3
        ), default=0, db_index=True)


class Operations(BaseRefHierarcy):
    code = CodeStrictField(unique=True)
    name = NameStrictField()
    props = OperationsManager.get_props()
    fullname = TextField()

    @property
    def attrs(self):
        from kaf_pas.production.models.operation_attr import Operation_attr
        return [item.attr_type.code for item in Operation_attr.objects.filter(operation=self)]

    @property
    def is_launched(self):
        return IsBitOn(self.props, Operations.props.launched)
        # return True

    @property
    def is_grouped(self):
        return IsBitOn(self.props, Operations.props.grouped)

    @property
    def is_transportation(self):
        return IsBitOn(self.props, Operations.props.transportation)

    @property
    def is_absorption(self):
        return IsBitOn(self.props, Operations.props.absorption)

    objects = OperationsManager()

    def __str__(self):
        return f'ID={self.id}, code={self.code}, name={self.name} , props={self.props} , description={self.description}'

    class Meta:
        verbose_name = 'Операции'
        db_constraints = {
            'Operations_not_cycled': 'CHECK ("id" != "parent_id")',
        }
