import logging

from django.db.models import DateTimeField, BigIntegerField, TextField, BooleanField

from isc_common.bit import IsBitOff
from isc_common.fields.code_field import CodeField
from isc_common.fields.description_field import DescriptionField
from isc_common.fields.name_field import NameField
from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.audit import AuditModel, AuditManager, AuditQuerySet
from isc_common.models.base_ref import Hierarcy
from kaf_pas.sales.models.precent_item_types import Precent_item_types
from kaf_pas.sales.models.precent_types import Precent_types
from kaf_pas.sales.models.status_precent import StatusPrecent

logger = logging.getLogger(__name__)


class Precent_viewQuerySet(AuditQuerySet):
    def filter(self, *args, **kwargs):
        return super().filter(*args, **kwargs)


class Precent_viewManager(AuditManager):

    @classmethod
    def getRecord(cls, record):
        res = {
            'id': record.id,
            'code': record.code,
            'date': record.date,
            'year': record.year,
            'month': record.month,
            'month_name': record.month_name,
            'date_sign': record.date_sign,
            'description': record.description,

            'status_id': record.status.id if record.status else None,
            'status__code': record.status.code if record.status else None,
            'status__name': record.status.name if record.status else None,

            'precent_item_type_id': record.precent_item_type.id if record.precent_item_type else None,
            'precent_item_type__code': record.precent_item_type.code if record.precent_item_type else None,
            'precent_item_type__name': record.precent_item_type.name if record.precent_item_type else None,

            'precent_type_id': record.precent_type.id if record.precent_type else None,
            'precent_type__code': record.precent_type.code if record.precent_type else None,
            'precent_type__name': record.precent_type.name if record.precent_type else None,

            'format': record.format,
            'mime_type': record.mime_type,
            'size': record.size if not str(record.size).startswith('.') else str(record.size).replace('.', '0.'),
            'real_name': record.real_name,

            'lastmodified': record.lastmodified,
            'editing': record.editing,
            'deliting': record.deliting,
            'parent_id': record.parent.id if record.parent else None,

            'isFolder': record.isFolder,
            'enabled': IsBitOff(record.status.props, 0),
        }
        return res

    def get_queryset(self):
        return Precent_viewQuerySet(self.model, using=self._db)


class Precent_view(Hierarcy):
    code = CodeField()
    isFolder = BooleanField()
    description = DescriptionField()

    date = DateTimeField(verbose_name='Дата', db_index=True)
    year = CodeField()
    month = CodeField()
    month_name = CodeField()
    date_sign = DateTimeField(verbose_name='Дата подписания', db_index=True, null=True, blank=True)

    size = BigIntegerField(verbose_name='Размер фала', default=0)
    real_name = TextField(verbose_name='Первоначальное имя файла', null=True, blank=True, default=None)
    mime_type = NameField(verbose_name='MIME тип файла файла', null=True, blank=True, default=None)
    format = NameField(verbose_name='Формат файла')

    status = ForeignKeyProtect(StatusPrecent)
    precent_item_type = ForeignKeyProtect(Precent_item_types, null=True, blank=True)
    precent_type = ForeignKeyProtect(Precent_types, null=True, blank=True)

    objects = Precent_viewManager()

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'Документы'
        db_table = 'sales_precent_view'
        managed = False
