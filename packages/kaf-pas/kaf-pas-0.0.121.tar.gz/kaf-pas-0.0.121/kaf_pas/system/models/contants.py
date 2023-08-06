import logging

from django.db.models import TextField, UniqueConstraint, Q
from django.forms import model_to_dict

from isc_common.fields.code_field import CodeStrictField
from isc_common.http.DSRequest import DSRequest
from isc_common.models.base_ref import BaseRefManager, BaseRefQuerySet, BaseRefHierarcy
from isc_common.number import DelProps

logger = logging.getLogger(__name__)


class ContantsQuerySet(BaseRefQuerySet):
    pass


class ContantsManager(BaseRefManager):

    @classmethod
    def getRecord(cls, record):
        res = {
            'id': record.id,
            'code': record.code,
            'name': record.name,
            'description': record.description,
            'value': record.value,
            'parent_id': record.parent.id if record.parent else None,
            'editing': record.editing,
            'deliting': record.deliting,
        }
        return res

    def get_queryset(self):
        return ContantsQuerySet(self.model, using=self._db)

    def createFromRequest(self, request, removed=None):
        request = DSRequest(request=request)
        data = request.get_data()
        _data = data.copy()
        self._remove_prop(_data, removed)

        res = super().create(**_data)
        res = model_to_dict(res)
        data.update(DelProps(res))
        return data

    # def updateFromRequest(self, request, removed=None):
    #     request = DSRequest(request=request)
    #     data = request.get_data()
    #     _data = data.copy()
    #     self._remove_prop(_data, removed)
    #
    #     isFolder = _data.get('isFolder', False)
    #     delAttr(_data, 'isFolder')
    #     id = _data.get('id')
    #     delAttr(_data, 'id')
    #     res = super().update_or_create(id=id, defaults=_data)
    #     data.setdefault('isFolder', isFolder)
    #     return data

    def refreshMatViewFromRequest(self, request):
        from kaf_pas.kd.models.lotsman_documents_hierarcy_ext import Lotsman_documents_hierarcyManagerExt

        if not isinstance(request, DSRequest):
            request = DSRequest(request=request)
        data = request.get_data()

        Lotsman_documents_hierarcyManagerExt(user=request.user).make_mview()

        return data

    def fixed_num_in_operationsFromRequest(self, request, removed=None, ):
        from kaf_pas.production.models.operations_item import Operations_itemManager
        request = DSRequest(request=request)

        res = dict(cnt=Operations_itemManager.refresh_num1())
        return res


class Contants(BaseRefHierarcy):
    code = CodeStrictField()
    value = TextField(null=True, blank=True, db_index=True)
    objects = ContantsManager()

    def __str__(self):
        return f'ID:{self.id}, code:{self.code}, name:{self.name}, description:{self.description}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Системные константы'
        constraints = [
            UniqueConstraint(fields=['code', 'value'], condition=Q(parent=None), name='Contants_unique_constraint_0'),
            UniqueConstraint(fields=['code', 'parent', 'value'], name='Contants_unique_constraint_1'),
        ]
