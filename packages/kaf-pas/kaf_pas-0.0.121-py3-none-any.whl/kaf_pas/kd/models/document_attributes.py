import logging
from typing import List

from django.db import transaction
from django.db.models import TextField, UniqueConstraint, Q, FloatField
from django.forms import model_to_dict

from isc_common import setAttr
from isc_common.common.functions import delete_dbl_spaces
from isc_common.fields.related import ForeignKeyProtect
from isc_common.http.DSRequest import DSRequest
from isc_common.logger.Logger import Logger
from isc_common.managers.common_managet_with_lookup_fields import CommonManagetWithLookUpFieldsManager, CommonManagetWithLookUpFieldsQuerySet
from isc_common.models.audit import AuditModel
from isc_common.number import DelProps, StrToNumber, StrToInt
from kaf_pas.ckk.models.attr_type import Attr_type, AttrManager

logger = logging.getLogger(__name__)
logger.__class__ = Logger


class Document_attributesQuerySet(CommonManagetWithLookUpFieldsQuerySet):

    def create(self, **kwargs):
        attr_type = kwargs.get('attr_type')
        if isinstance(attr_type, Attr_type):
            value_str = kwargs.get('value_str')
            if value_str is not None:
                setAttr(kwargs, 'value_str', value_str.strip())
            return super().create(**kwargs)

        value_str = kwargs.get('value_str').strip()
        value_int = StrToInt(value_str)

        if not kwargs.get('attr_type_id'):
            attr_type, _ = Attr_type.objects.get_or_create(code=kwargs.get('attr_type__code'))
            setAttr(kwargs, 'attr_type_id', attr_type.id)
        setAttr(kwargs, 'value_int', value_int)
        setAttr(kwargs, 'value_str', value_str)

        return super().create(**kwargs)

    def get_or_create(self, defaults=None, **kwargs):
        attr_type = kwargs.get('attr_type')
        if isinstance(attr_type, Attr_type):
            value_str = kwargs.get('value_str')
            if value_str is not None:
                setAttr(kwargs, 'value_str', value_str.strip())
            return super().get_or_create(defaults, **kwargs)

        value_str = kwargs.get('value_str')
        if value_str is not None:
            value_str = value_str.strip()

        if not kwargs.get('attr_type_id') and kwargs.get('attr_type__code'):
            attr_type, _ = Attr_type.objects.get_or_create(code=kwargs.get('attr_type__code'))
            setAttr(kwargs, 'attr_type_id', attr_type.id)
        elif isinstance(defaults, dict) and not defaults.get('attr_type_id') and defaults.get('attr_type__code'):
            attr_type, _ = Attr_type.objects.get_or_create(code=defaults.get('attr_type__code'))
            setAttr(kwargs, 'attr_type_id', attr_type.id)

        if not value_str and isinstance(defaults, dict):
            value_str = defaults.get('value_str').strip()
            value_int = StrToInt(value_str)
            setAttr(defaults, 'value_int', value_int)
            setAttr(defaults, 'value_str', value_str)
        else:
            value_int = StrToInt(value_str)
            setAttr(kwargs, 'value_int', value_int)
            setAttr(kwargs, 'value_str', value_str)

        return super().get_or_create(defaults, **kwargs)

    def update(self, **kwargs):
        attr_type = kwargs.get('attr_type')
        if isinstance(attr_type, Attr_type):
            return super().update(**kwargs)

        value_str = kwargs.get('value_str')
        value_int = StrToInt(value_str)
        if not kwargs.get('attr_type_id'):
            attr_type, _ = Attr_type.objects.get_or_create(code=kwargs.get('attr_type__code'))
            setAttr(kwargs, 'attr_type_id', attr_type.id)
        setAttr(kwargs, 'value_int', value_int)

        return super().update(**kwargs)

    def update_or_create(self, defaults=None, **kwargs):
        attr_type = kwargs.get('attr_type')
        if isinstance(attr_type, Attr_type):
            return super().update_or_create(defaults, **kwargs)

        value_str = kwargs.get('value_str')

        if not kwargs.get('attr_type_id') and kwargs.get('attr_type__code'):
            attr_type, = Attr_type.objects.get_or_create(code=kwargs.get('attr_type__code'))
            setAttr(kwargs, 'attr_type_id', attr_type.id)
        elif isinstance(defaults, dict) and not defaults.get('attr_type_id') and defaults.get('attr_type__code'):
            attr_type, _ = Attr_type.objects.get_or_create(code=defaults.get('attr_type__code'))
            setAttr(kwargs, 'attr_type_id', attr_type.id)

        if not value_str and isinstance(defaults, dict):
            value_str = defaults.get('value_str')
            value_int = StrToInt(value_str)
            setAttr(defaults, 'value_int', value_int)
        else:
            value_int = StrToInt(value_str)
            setAttr(kwargs, 'value_int', value_int)

        return super().update_or_create(defaults, **kwargs)


class Document_attributesManager(CommonManagetWithLookUpFieldsManager):
    @classmethod
    def get_or_create_attribute(cls, attr_codes, value_str, attr_names=None, logger=None):
        from django.conf import settings

        key = 'Document_attributesManager.get_or_create_attribute'
        settings.LOCKS.acquire(key)
        attr_type = AttrManager.get_or_create_attr(attr_codes=attr_codes, attr_names=attr_names, logger=logger)
        value_int = StrToNumber(value_str)

        try:
            attribute = Document_attributes.objects.filter(
                value_str__delete_dbl_spaces=delete_dbl_spaces(value_str),
                attr_type=attr_type,
            ).order_by('id')[0]
            settings.LOCKS.release(key)
            return attribute, False
        except IndexError:
            attribute = Document_attributes.objects.create(
                attr_type=attr_type,
                value_str=delete_dbl_spaces(value_str),
                value_int=value_int
            )
            settings.LOCKS.release(key)
            return attribute, True

    def get_queryset(self):
        return Document_attributesQuerySet(self.model, using=self._db)

    @classmethod
    def getRecord(cls, record):
        res = {
            "id": record.id,
            "attr_type_id": record.attr_type.id,
            "attr_type__code": record.attr_type.code,
            "attr_type__name": record.attr_type.name,
            "attr_type__description": record.attr_type.description,
            "value_str": record.value_str.strip() if isinstance(record.value_str, str) else None,
            "value_int": record.value_int,
            "lastmodified": record.lastmodified,
            "editing": record.editing,
            "deliting": record.deliting,
        }
        return res

    def update_document_attributes(self, document_attribute):
        with transaction.atomic():
            document_attributes = Document_attributes.objects.get(id=document_attribute.get('id'))
            document_attributes.value_str = document_attribute.get('value_str').strip()
            if document_attribute.get('value_int') is not None:
                document_attributes.value_int = document_attribute.get('value_int')
            else:
                document_attributes.value_int = StrToNumber(document_attribute.get('value_str').strip())
            document_attributes.save()
            return document_attribute

    def updateFromRequest(self, request, removed=None, function=None):
        if not isinstance(request, DSRequest):
            request = DSRequest(request=request)
        data = request.get_data()
        return self.update_document_attributes(data)

    def createFromRequest(self, request, removed=None, propsArr: List = None):
        request = DSRequest(request=request)
        data = request.get_data()

        if data.get('value_int') is not None and data.get('value_str') is None:
            setAttr(data, 'value_str', str(data.get('value_int')))
        elif data.get('value_int') is None and data.get('value_str') is not None:
            setAttr(data, 'value_int', StrToNumber(data.get('value_str')))

        _data = data.copy()
        self._remove_prop(_data, removed)

        props = self.get_prp(data=_data, propsArr=propsArr)
        if props > -1:
            setAttr(_data, 'props', props)
        res = super().create(**_data)
        if data.get('value_int') is not None:
            res.value_int = _data.get('value_int')
            res.save()

        res = model_to_dict(res)
        data.update(DelProps(res))
        return data

    def deleteFromRequest(self, request, removed=None, ):
        from kaf_pas.kd.models.document_attr_cross import Document_attr_cross

        request = DSRequest(request=request)
        res = 0
        tuple_ids = request.get_tuple_ids()
        with transaction.atomic():
            for id, mode in tuple_ids:
                if mode == 'hide':
                    super().filter(id=id).soft_delete()
                elif mode == 'visible':
                    super().filter(id=id).soft_restore()
                else:
                    Document_attr_cross.objects.filter(attribute_id=id).delete()
                    qty, _ = super().filter(id=id).delete()
                res += qty
        return res


class Document_attributes(AuditModel):
    attr_type = ForeignKeyProtect(Attr_type, verbose_name='Тип атрибута')
    value_str = TextField(verbose_name="Значение атрибута", db_index=True, null=True, blank=True)
    value_int = FloatField(verbose_name="Значение атрибута", db_index=True, null=True, blank=True)

    objects = Document_attributesManager()

    def __str__(self):
        return f'ID={self.id}, attr_type=[{self.attr_type}], value_str={self.value_str}, value_int={self.value_int}'

    class Meta:
        verbose_name = 'Аттрибуты докуменнта'
        constraints = [
            UniqueConstraint(fields=['attr_type', 'value_str'], condition=Q(value_int=None), name='Document_attributes_unique_constraint_0'),
            UniqueConstraint(fields=['attr_type', 'value_int', 'value_str'], name='Document_attributes_unique_constraint_1'),
        ]
