import logging

from bitfield import BitField
from django.db.models import DecimalField
from django.forms import model_to_dict

from isc_common import setAttr, delAttr
from isc_common.bit import IsBitOn
from isc_common.fields.code_field import CodeStrictField
from isc_common.http.DSRequest import DSRequest
from isc_common.managers.common_managet_with_lookup_fields import CommonManagetWithLookUpFieldsManager, CommonManagetWithLookUpFieldsQuerySet
from isc_common.models.base_ref import BaseRefHierarcy, BaseRefQuerySet
from isc_common.number import DelProps, GetPropsInt, DecimalToStr

logger = logging.getLogger(__name__)


class Ed_izmQuerySet(BaseRefQuerySet, CommonManagetWithLookUpFieldsQuerySet):
    pass


class Ed_izmManager(CommonManagetWithLookUpFieldsManager):

    @classmethod
    def getRecord(cls, record):
        res = {
            'id': record.id,
            'code': record.code,
            'name': record.name,
            'koef_recalc': DecimalToStr(record.koef_recalc),
            'description': record.description,
            'parent_id': record.parent.id if record.parent else None,
            'editing': record.editing,
            'deliting': record.deliting,
            'props': GetPropsInt(record.props),
            'root_timevalue': IsBitOn(record.props, 0)
        }
        return res

    def createFromRequest(self, request):
        request = DSRequest(request=request)
        data = request.get_data()
        _data = data.copy()

        props = 0
        if _data.get('root_timevalue') is not None and isinstance(_data.get('root_timevalue'), bool):
            if _data.get('root_timevalue'):
                props |= Ed_izm.props.root_timevalue
            else:
                props &= ~Ed_izm.props.root_timevalue

            delAttr(_data, 'root_timevalue')
            setAttr(_data, 'props', props)

        res = super().create(**_data)
        res = model_to_dict(res)
        setAttr(res, 'full_name', res.full_name)

        setAttr(res, 'isFolder', False)
        data.update(DelProps(res))
        return data

    def updateFromRequest(self, request, removed=None, function=None):
        if not isinstance(request, DSRequest):
            request = DSRequest(request=request)
        data = request.get_data()

        _data = data.copy()
        _data1 = _data.copy()

        props = DelProps(_data).get('props')

        if _data.get('root_timevalue') is not None and isinstance(_data.get('root_timevalue'), bool):
            if _data.get('root_timevalue'):
                props |= Ed_izm.props.root_timevalue
            else:
                props &= ~Ed_izm.props.root_timevalue

            delAttr(_data, 'root_timevalue')
            setAttr(_data, 'props', props)

        super().filter(id=request.get_id()).update(**_data)
        return _data1

    def get_queryset(self):
        return Ed_izmQuerySet(self.model, using=self._db)


class Ed_izm(BaseRefHierarcy):
    code = CodeStrictField(unique=True)
    koef_recalc = DecimalField(max_digits=19, decimal_places=4, null=True, blank=True)

    props = BitField(flags=(
        ('root_timevalue', 'Базовая временная единица'),  # 1
    ), default=0, db_index=True)

    objects = Ed_izmManager()

    @classmethod
    def root_timevalue(cls):
        return Ed_izm.objects.get(props=Ed_izm.props.root_timevalue)

    def __str__(self):
        return f"ID: {self.id}, code: {self.code}, koef_recalc: {self.koef_recalc}"

    class Meta:
        verbose_name = 'Единицы измерения'
