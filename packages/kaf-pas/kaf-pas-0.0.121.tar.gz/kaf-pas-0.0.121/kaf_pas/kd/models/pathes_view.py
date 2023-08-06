import logging
import os

from django.db.models import TextField, BigAutoField, DateTimeField, BooleanField, Model, CharField
from django.utils import timezone

from isc_common.fields.related import ForeignKeyProtect
from isc_common.number import DelProps
from kaf_pas.ckk.models.attr_type import Attr_type
from kaf_pas.kd.models.pathes import Pathes, PathesManager

logger = logging.getLogger(__name__)


class Pathes_viewManager(PathesManager):

    @classmethod
    def getRecord(cls, record):
        res = {
            "absolute_path": record.absolute_path,
            "attr_type__code": record.attr_type.code if record.attr_type else None,
            "attr_type__name": record.attr_type.name if record.attr_type else None,
            "attr_type_id": record.attr_type.id if record.attr_type else None,
            "deliting": record.deliting,
            "drive": record.drive,
            "editing": record.editing,
            "enable_upload": record.props.enable_upload,
            "id": record.id,
            "isFolder": record.isFolder,
            "isUpload": record.isUpload,
            "lastmodified": record.lastmodified,
            "parent_id": record.parent_id,
            "path": record.path,
            "props": record.props,
            "virt_path": record.virt_path,
        }
        return DelProps(res)


class Pathes_view(Model):
    id = BigAutoField(primary_key=True, verbose_name="Идентификатор")
    deleted_at = DateTimeField(verbose_name="Дата мягкого удаления", null=True, blank=True, db_index=True)
    editing = BooleanField(verbose_name="Возможность редактирования", default=True)
    deliting = BooleanField(verbose_name="Возможность удаления", default=True)
    lastmodified = DateTimeField(verbose_name='Последнее обновление', editable=False, db_index=True, default=timezone.now)

    isFolder = BooleanField(null=True, blank=True, )
    isUpload = BooleanField(null=True, blank=True, )

    drive = CharField(max_length=10, null=True, blank=True)
    path = TextField(verbose_name="Путь")
    absolute_path = TextField(verbose_name="Абсолютный Путь")
    virt_path = TextField(verbose_name="Мнимый путь", null=True, blank=True)
    parent = ForeignKeyProtect("self", null=True, blank=True)
    attr_type = ForeignKeyProtect(Attr_type, verbose_name='Атрибут', null=True, blank=True)

    props = PathesManager.props()

    @property
    def drived_absolute_path(self):
        drive = self.get_drive(self.id)
        if drive:
            return f'{drive}{self.absolute_path}'
        else:
            return self.absolute_path

    def __str__(self):
        return f"ID: {self.id}, drive: {self.drive}, virt_path: {self.virt_path}, attr_type: [{self.attr_type}] absolute_path: {self.absolute_path}"

    objects = Pathes_viewManager()

    class Meta:
        db_table = 'kd_pathes_view'
        managed = False
        verbose_name = 'Пути нахождения документов'
