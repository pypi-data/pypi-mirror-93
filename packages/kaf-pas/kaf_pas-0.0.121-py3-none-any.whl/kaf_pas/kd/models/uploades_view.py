import logging

from bitfield import BitField
from django.conf import settings
from django.db import transaction
from django.db.models import TextField

from isc_common import delAttr
from isc_common.bit import TurnBitOn
from isc_common.common import blinkString
from isc_common.common.mat_views import refresh_mat_view
from isc_common.datetime import DateTimeToStr
from isc_common.fields.related import ForeignKeyProtect
from isc_common.http.DSRequest import DSRequest
from isc_common.models.audit import AuditModel, AuditManager, AuditQuerySet
from isc_common.number import DelProps
from isc_common.progress import managed_progress, ProgressDroped, progress_deleted
from kaf_pas.kd.models.pathes import Pathes
from kaf_pas.kd.models.uploades import UploadesManager

logger = logging.getLogger(__name__)


class Uploades_viewQuerySet(AuditQuerySet):
    def get_info(self, request, *args):
        request = DSRequest(request=request)
        criteria = self.get_criteria(json=request.json)
        cnt = super().filter(*args, criteria).count()
        cnt_all = super().filter().count()
        return dict(qty_rows=cnt, all_rows=cnt_all)


class Uploades_viewManager(AuditManager):

    @classmethod
    def getRecord(cls, record):
        res = {
            'id': record.id,
            'lastmodified': record.lastmodified,
            'path_id': record.path.id,
            'absolute_path': record.absolute_path,
            'editing': record.editing,
            'deliting': record.deliting,
            'props': record.props,
            'confirmed': record.props.confirmed,
        }
        return DelProps(res)

    def get_queryset(self):
        return Uploades_viewQuerySet(self.model, using=self._db)

class Uploades_view(AuditModel):
    path = ForeignKeyProtect(Pathes)
    absolute_path = TextField(verbose_name="Абсолютный Путь")

    props = UploadesManager.props()

    objects = Uploades_viewManager()

    def __str__(self):
        return f"{self.id}, path: [{self.path}]"

    class Meta:
        verbose_name = 'Загрузки внешних данных'
        managed=False
        db_table='kd_uploades_view'
