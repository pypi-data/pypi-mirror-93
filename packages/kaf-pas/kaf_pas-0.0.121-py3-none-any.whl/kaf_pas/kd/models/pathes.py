import logging
import os

from bitfield import BitField
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import TextField, CharField, UniqueConstraint, Q

from isc_common import delete_drive_leter, get_drive_leter
from isc_common.bit import TurnBitOn
from isc_common.common.mat_views import refresh_mat_view
from isc_common.fields.related import ForeignKeyProtect
from isc_common.http.DSRequest import DSRequest
from isc_common.managers.common_managet_with_lookup_fields import CommonManagetWithLookUpFieldsManager, CommonManagetWithLookUpFieldsQuerySet
from isc_common.models.base_ref import Hierarcy
from isc_common.models.tree_audit import TreeAuditModelManager
from isc_common.progress import managed_progress, ProgressDroped, progress_deleted
from kaf_pas.ckk.models.attr_type import Attr_type

logger = logging.getLogger(__name__)


class PathesQuerySet(CommonManagetWithLookUpFieldsQuerySet):
    def delete(self):
        from kaf_pas.kd.models.documents import Documents

        for item in self:
            Documents.objects.filter(path=item).delete()

        return super().delete()


class PathesManager(CommonManagetWithLookUpFieldsManager):
    @classmethod
    def props(cls):
        return BitField(flags=(
            ('enable_upload', 'Директория для закачки'),
        ), default=1, db_index=True)

    def get_queryset(self):
        return PathesQuerySet(self.model, using=self._db)

    @classmethod
    def getRecord(cls, record):
        res = {
            "id": record.id,
            "path": record.path,
            "virt_path": record.virt_path,
            "parent_id": record.parent_id,
            "lastmodified": record.lastmodified,
            "editing": record.editing,
            "drive": record.drive,
            "deliting": record.deliting,
            "attr_type_id": record.attr_type.id if record.attr_type else None,
            "attr_type__code": record.attr_type.code if record.attr_type else None,
            "attr_type__name": record.attr_type.name if record.attr_type else None,
            # "isFolder": record.isFolder,
        }
        return res

    @property
    def sep(self):
        return os.altsep if os.altsep else os.sep

    def create_ex(self, **kwargs):
        path = kwargs.get('path')
        parent = kwargs.get('parent')
        with_out_last = kwargs.get('with_out_last')

        if not path:
            raise Exception(f'path {path} is not exists.')

        if path:
            drive = get_drive_leter(path)
            path = delete_drive_leter(path)

            if path != '':
                if with_out_last:
                    path_items = path.split(self.sep)[: - 1]
                else:
                    path_items = path.split(self.sep)

                for path_item in path_items:
                    if path_item:
                        alive_only = self.alive_only
                        try:
                            self.alive_only = False
                            if drive and path == '':
                                parent = super().get(drive=drive, path=path_item, parent=parent)
                            else:
                                parent = super().get(path=path_item, parent=parent)
                            self.alive_only = alive_only
                        except ObjectDoesNotExist:
                            self.alive_only = alive_only
                            if drive and path == '':
                                parent = super().create(drive=drive, path=path_item, parent=parent)
                            else:
                                parent = super().create(path=path_item, parent=parent)
            else:
                parent, _ = super().get_or_create(drive=drive, parent=parent)

        return parent

    def create_ex1(self, **kwargs):
        path = kwargs.get('path')
        parent = kwargs.get('parent')
        with_out_last = kwargs.get('with_out_last')

        if not path:
            raise Exception(f'path {path} is not exists.')

        if path:
            drive = get_drive_leter(path)
            path = delete_drive_leter(path)

            if path != '':
                if with_out_last:
                    path_items = path.split(self.sep)
                else:
                    path_items = path.split(self.sep)

                for path_item in path_items:
                    if path_item:
                        alive_only = self.alive_only
                        try:
                            self.alive_only = False
                            if drive and path == '':
                                parent = super().get(drive=drive, path=path_item, parent=parent)
                            else:
                                parent = super().get(path=path_item, parent=parent)
                            self.alive_only = alive_only
                        except ObjectDoesNotExist:
                            self.alive_only = alive_only
                            if drive and path == '':
                                parent = super().create(drive=drive, path=path_item, parent=parent)
                            else:
                                parent = super().create(path=path_item, parent=parent)
            else:
                parent, _ = super().get_or_create(drive=drive, parent=parent)

        return parent

    # Только для перенаправленных на виндовый сервак вызовов !!!!
    def deleteFromRequest(self, request, removed=None, ):
        from django.db import transaction
        from isc_common.auth.models.user import User
        from kaf_pas.kd.models.documents import DocumentManager
        from kaf_pas.kd.models.documents import Documents
        from kaf_pas.kd.models.uploades import Uploades
        from kaf_pas.kd.models.uploades_documents import Uploades_documents
        from kaf_pas.kd.models.uploades_log import Uploades_log

        ids = request.GET.getlist('ids')
        request = DSRequest(request=request)

        res = 0
        count = 0
        lotsman_count = 0

        for i in range(0, len(ids), 2):
            with transaction.atomic():
                if ids[i + 1] == 'hide':
                    res += super().filter(id=ids[i]).soft_delete()
                else:
                    cnt = Pathes.objects_tree.get_descendants_count(
                        id=ids[i],
                        child_id='id')

                    with managed_progress(
                            id='delete_pathes',
                            qty=cnt - 1,
                            user=request.user,
                            message='Удаление путей размещения.',
                            title='Выполнено',
                            props=TurnBitOn(0, 0)
                    ) as progress:

                        for path in Pathes.objects_tree.get_descendants(
                                id=ids[i],
                                child_id='id',
                                order_by_clause='order by level desc'):

                            for upload in Uploades.objects.filter(path=path.id):
                                Uploades_log.objects.filter(upload=upload).delete()
                                Uploades_documents.objects.filter(upload=upload).delete()
                                upload.delete()

                            for document in Documents.objects.filter(path_id=path.id):
                                count, lotsman_count = DocumentManager.delete(document.id, request.user)

                            res += super().filter(id=path.id).delete()[0]
                            logger.debug(f'Deleted: {res}')
                            step_res = progress.step()

                            if step_res != 0:
                                raise ProgressDroped(progress_deleted)
        if count > 0:
            refresh_mat_view('kd_documents_mview')
        if lotsman_count > 0:
            refresh_mat_view('kd_lotsman_documents_hierarcy_mview')
        return res

    def get_drive(self, id):
        try:
            path = self.get(id=id)
            if path.drive:
                return path.drive
            elif path.parent:
                return self.get_drive(path.parent.id)
            else:
                return path.drive
        except Pathes.DoesNotExist:
            return None


class Pathes(Hierarcy):
    attr_type = ForeignKeyProtect(Attr_type, verbose_name='Атрибут', null=True, blank=True)
    drive = CharField(verbose_name='Диск', max_length=10, null=True, blank=True)
    path = TextField(verbose_name="Путь")
    props = PathesManager.props()
    virt_path = TextField(verbose_name="Мнимый путь", null=True, blank=True)

    @property
    def sep(self):
        return os.altsep if os.altsep else os.sep

    def get_virt_path(self, id=None):
        try:
            path = Pathes.objects.get(id=id if id else self.id)
            if path.virt_path:
                return path.virt_path
            elif path.parent:
                return self.get_virt_path(path.parent.id)
            else:
                return path.virt_path
        except Pathes.DoesNotExist:
            return None

    @property
    def absolute_path(self):
        def get_parent(item_tuple):
            if item_tuple[0].parent:
                res = Pathes.objects.get(id=item_tuple[0].parent.id)
                res = (res, f"{res.path}/{item_tuple[1]}")
                return get_parent(res)
            else:
                return item_tuple

        if self.parent:
            res = get_parent((self, self.path))
            return f'{self.sep}{res[1]}'
        else:
            return f'{self.sep}{self.path}'

    def get_drive(self, id=None):
        try:
            path = Pathes.objects.get(id=id if id else self.id)
            if path.drive:
                return path.drive
            elif path.parent:
                return self.get_drive(path.parent.id)
            else:
                return path.drive
        except Pathes.DoesNotExist:
            return None

    @property
    def drived_absolute_path(self):
        drive = self.get_drive(self.id)
        if drive:
            return f'{drive}{self.absolute_path}'
        else:
            return self.absolute_path

    def __str__(self):
        return f"ID: {self.id}, drive: {self.drive}, virt_path: {self.virt_path}, attr_type: [{self.attr_type}] absolute_path: {self.absolute_path}"

    objects = PathesManager()
    objects_tree = TreeAuditModelManager()

    class Meta:
        db_table = 'pathes'
        verbose_name = 'Пути нахождения документов'
        constraints = [
            UniqueConstraint(fields=['id'], condition=Q(parent=None), name='Pathes_unique_constraint_0'),
            UniqueConstraint(fields=['id', 'parent'], name='Pathes_unique_constraint_1'),
        ]
