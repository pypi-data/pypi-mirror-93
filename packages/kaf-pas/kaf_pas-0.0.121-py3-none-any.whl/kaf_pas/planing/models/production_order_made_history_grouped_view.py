import logging

from django.conf import settings
from django.db.models import DateTimeField, BigIntegerField

from isc_common.auth.models.user import User
from isc_common.bit import TurnBitOn
from isc_common.common import black, blinkString
from isc_common.datetime import DateTimeToStr
from isc_common.fields.name_field import NameField
from isc_common.fields.related import ForeignKeyProtect
from isc_common.http.DSRequest import DSRequest
from isc_common.managers.common_manager import CommonManager
from isc_common.models.audit import AuditQuerySet, AuditModel
from isc_common.progress import managed_progress, ProgressDroped, progress_deleted
from isc_common.ws.webSocket import WebSocket
from kaf_pas.planing.models.production_order_values_ext import Production_order_values_ext

logger = logging.getLogger(__name__)


class Production_order_made_history_grouped_viewQuerySet(AuditQuerySet):
    pass


class Production_order_made_history_grouped_viewManager(CommonManager):
    production_order_values_ext = Production_order_values_ext()

    def get_queryset(self):
        return Production_order_made_history_grouped_viewQuerySet(self.model, using=self._db)

    @classmethod
    def getRecord(cls, record):
        res = {
            'id': record.id,
            'exucutor_id': record.exucutor.id,
            'short_name': record.short_name,
            'create_date': record.create_date,
            'process': record.process
        }
        return res

    @classmethod
    def fullRows(cls, suffix=''):
        WebSocket.full_refresh_grid(grid_id=f'{settings.GRID_CONSTANTS.refresh_ProductionOrderMadeHistory_grouped_grid}{suffix}')

    def delete_sums(self, maked_values, end_func_refreshed):
        operations = list(map(lambda x: x.operation, maked_values))

        def func_refreshed(_, key_lock):
            if callable(end_func_refreshed):
                end_func_refreshed(maked_values, key_lock)

        self.production_order_values_ext.delete_sums(operations=operations, end_func_refreshed=func_refreshed)

    def deleteFromRequest(self, request, removed=None, ):
        from django.db import transaction
        from kaf_pas.planing.models.production_order import Production_orderManager
        from kaf_pas.planing.models.production_order_made_history import Production_order_made_history
        from kaf_pas.planing.models.production_order_made_history import Production_order_made_historyManager
        from kaf_pas.planing.models.production_order_made_history_operations import Production_order_made_history_operations
        from kaf_pas.accounting.models.buffers import BuffersManager

        request = DSRequest(request=request)
        res = 0
        tuple_ids = request.get_olds_tuple_ids()

        with managed_progress(
                id=f'deleteFromRequest_{request.user.id}',
                qty=len(tuple_ids),
                user=request.user,
                message='Удаление данных по выпуску.',
                title='Выполнено',
                props=TurnBitOn(0, 0)
        ) as progress:
            with transaction.atomic():
                for id, mode in tuple_ids:
                    maked_values = list(Production_order_made_history_operations.objects.filter(production_order_made_history__process=id).order_by('-operation_id'))

                    def func_refreshed(maked_values, key_lock):
                        ids = list(set(map(lambda x: x.production_order_made_history.id_real, maked_values)))

                        Production_orderManager.update_redundant_planing_production_order_table(ids=ids, user=request.user)

                        if progress.step() != 0:
                            settings.LOCKS.release(key_lock)
                            raise ProgressDroped(progress_deleted)

                        Production_order_made_history.objects.filter(process=id).delete()
                        if len(ids) > 0:
                            Production_order_made_history_grouped_viewManager.fullRows()
                            Production_order_made_historyManager.fullRows()
                            BuffersManager.fullRows()

                    progress.setContentsLabel(content=blinkString(text=f'Удаление данных по выпуску ID={id}', blink=False, color=black, bold=True))

                    self.delete_sums(maked_values=maked_values, end_func_refreshed=func_refreshed)

        return res


class Production_order_made_history_grouped_view(AuditModel):
    create_date = DateTimeField(db_index=True)
    exucutor = ForeignKeyProtect(User)
    short_name = NameField()
    process = BigIntegerField(db_index=True)

    objects = Production_order_made_history_grouped_viewManager()

    # started = Status_operation_types.objects.get(code='started')

    def __str__(self):
        return f'\ncreate_date: {self.create_date}, ' \
               f'\ncreate_date: {DateTimeToStr(self.create_date)}, ' \
               f'\ncreator: [{self.exucutor}], ' \
               f'\nprocess: {self.process}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Выполнения по Заказам на производство'
        managed = False
        db_table = 'planing_production_order_made_history_grouped_view'
