import logging

from bitfield import BitField
from django.conf import settings
from django.db import transaction
from django.db.models import BigIntegerField, deletion

from isc_common.fields.related import ForeignKeyProtect
from isc_common.http.DSRequest import DSRequest
from isc_common.logger.Logger import Logger
from isc_common.models.audit import AuditManager, AuditQuerySet, AuditModel
from kaf_pas.ckk.models.attr_type import Attr_type
from kaf_pas.kd.models.documents import Documents

logger = logging.getLogger(__name__)
logger.__class__ = Logger


class Lotsman_documents_hierarcyQuerySet(AuditQuerySet):
    pass


class Lotsman_documents_hierarcyManager(AuditManager):

    @classmethod
    def delete(cls, id, user):
        from isc_common.auth.models.user import User
        from kaf_pas.ckk.models.item import Item
        from kaf_pas.ckk.models.item import ItemManager
        from kaf_pas.kd.models.documents_thumb import Documents_thumb
        from kaf_pas.kd.models.documents_thumb10 import Documents_thumb10
        from kaf_pas.kd.models.lotsman_document_attr_cross import Lotsman_document_attr_cross
        from kaf_pas.kd.models.lotsman_documents_hierarcy_files import Lotsman_documents_hierarcy_files

        if not isinstance(user, User):
            raise Exception('user  must be a User instance.')

        res = 0

        key = 'Lotsman_documents_hierarcyManager.delete'
        settings.LOCKS.acquire(key)
        Documents_thumb.objects.filter(lotsman_document_id=id).delete()
        Documents_thumb10.objects.filter(lotsman_document_id=id).delete()
        Lotsman_document_attr_cross.objects.filter(document_id=id).delete()

        for item in Item.objects.filter(lotsman_document_id=id):
            ItemManager.delete_recursive(item_id=item.id, user=user)

        Lotsman_documents_hierarcy_files.objects.filter(lotsman_document_id=id).delete()
        try:
            res += Lotsman_documents_hierarcy.objects.filter(id=id).delete()[0]
        except deletion.ProtectedError:
            pass
        settings.LOCKS.release(key)
        return res

    @classmethod
    def delete_file(cls, id, user):
        from isc_common.auth.models.user import User
        from kaf_pas.kd.models.documents_thumb import Documents_thumb
        from kaf_pas.kd.models.documents_thumb10 import Documents_thumb10
        from kaf_pas.kd.models.lotsman_documents_hierarcy_files import Lotsman_documents_hierarcy_files
        from django.conf import settings

        key = 'Lotsman_documents_hierarcyManager.delete_file'
        settings.LOCKS.acquire(key)

        if not isinstance(user, User):
            raise Exception('user  must be a User instance.')

        res = 0

        res += Documents_thumb.objects.filter(lotsman_document_id=id).delete()[0]
        res += Documents_thumb10.objects.filter(lotsman_document_id=id).delete()[0]

        res += Lotsman_documents_hierarcy_files.objects.filter(lotsman_document_id=id).delete()[0]
        settings.LOCKS.release(key)
        return res

    @classmethod
    def get_props(cls):
        return BitField(flags=(
            ('relevant', 'Актуальность'),
            ('beenItemed', 'Был внесен в состав изделий'),
        ), default=1, db_index=True)

    @classmethod
    def getRecord(cls, record):
        res = {
            'id': record.id,
            'editing': record.editing,
            'deliting': record.deliting,
        }
        return res

    def makeItemFromRequest(self, request):
        from kaf_pas.kd.models.lotsman_documents_hierarcy_view import Lotsman_documents_hierarcy_view
        from kaf_pas.kd.models.lotsman_documents_hierarcy_ext import Lotsman_documents_hierarcyManagerExt
        from kaf_pas.kd.models.documents_ext import DocumentManagerExt

        request = DSRequest(request=request)
        data = request.get_data()

        Lotsman_documents_hierarcyManagerExt(
            user=request.user,
            documentManagerExt=DocumentManagerExt(logger=logger)).make_items(lotsman_documents_hierarcy_view_record=Lotsman_documents_hierarcy_view.objects.get(id=data.get('id')))

        return data

    def get_queryset(self):
        return Lotsman_documents_hierarcyQuerySet(self.model, using=self._db)

    def deleteFromRequest(self, request, removed=None, ):
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
                    qty, _ = super().filter(id=id).delete()
                res += qty
        return res


class Lotsman_documents_hierarcy(AuditModel):
    id = BigIntegerField(primary_key=True, verbose_name="Идентификатор")
    attr_type = ForeignKeyProtect(Attr_type, verbose_name='Тип документа')
    document = ForeignKeyProtect(Documents)

    props = Lotsman_documents_hierarcyManager.get_props()

    objects = Lotsman_documents_hierarcyManager()

    def __str__(self):
        return f'ID:{self.id}, attr_type: [{self.attr_type}], document: [{self.document}], props: {self.props}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Иерархия документа из Лоцмана'
