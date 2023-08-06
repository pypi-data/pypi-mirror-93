import logging

from bitfield import BitField
from django.conf import settings
from django.db import transaction
from django.db.models import Q, UniqueConstraint, CheckConstraint, F, BigIntegerField

from isc_common import Wrapper, delAttr
from isc_common.bit import TurnBitOn
from isc_common.common import blinkString
from isc_common.fields.related import ForeignKeyProtect
from isc_common.http.DSRequest import DSRequest
from isc_common.models.audit import AuditQuerySet, AuditManager, AuditModel
from isc_common.models.tree_audit import TreeAuditModelManager
from isc_common.number import DelProps, model_2_dict
from isc_common.progress import managed_progress, ProgressDroped, progress_deleted
from kaf_pas.ckk.models.item import Item
from kaf_pas.ckk.models.locations import Locations

logger = logging.getLogger(__name__)


class RecordWrapper(Wrapper):
    child_id = None
    parent_id = None


class DataWrapper(Wrapper):
    targetRecord = dict()
    dropRecords = []
    mode = None
    location = None


class Item_refs_locationQuerySet(AuditQuerySet):
    pass


class Item_refs_locationManager(AuditManager):
    @classmethod
    def props(cls):
        return BitField(flags=(
            ('used', 'Используемость в группировке заданий на производство'),  # 2
        ), default=1, db_index=True)

    @classmethod
    def getRecord(cls, record):
        res = {
            'id': record.id,
            'child_id': record.child.id,
            'parent_id': record.parent.id if record.parent else None,
            'editing': record.editing,
            'deliting': record.deliting,
            'props': record.props,
        }
        return DelProps(res)

    def get_queryset(self):
        return Item_refs_locationQuerySet(self.model, using=self._db)

    def updateFromRequest(self, request, removed=None, function=None):
        from kaf_pas.ckk.models.item_refs import Item_refs
        from kaf_pas.ckk.models.item_refs_location_view import Item_refs_location_viewManager

        request = DSRequest(request=request)
        data = request.get_data()
        old_data = request.get_old_data()

        _data = data.copy()
        _data = DataWrapper(**data)

        mode = _data.mode
        targetRecord = RecordWrapper(**_data.targetRecord)
        parent_id = targetRecord.child_id

        key = None
        if _data.location is not None:
            location = Wrapper(**_data.location)
            key = f'grouping_{location.id}'
            settings.LOCKS.acquire(key)

        with transaction.atomic():
            if mode == 'insert':
                for dropRecord in map(lambda dropRecord: RecordWrapper(**dropRecord), _data.dropRecords):

                    item_refs = list(Item_refs.objects.get_descendants(where_clause0=f'child_id={dropRecord.id} and parent_id={dropRecord.parent_id}'))
                    with managed_progress(
                            id=key,
                            qty=len(item_refs),
                            user=request.user,
                            message='Перенос данных',
                            title='Выполнено',
                            props=TurnBitOn(0, 0)
                    ) as progress:

                        def except_func():
                            settings.LOCKS.release(key)

                        progress.except_func = except_func
                        for item_ref in item_refs:
                            progress.setContentsLabel(blinkString(text=f'Перенос {item_ref.child.item_name}', blink=False, color="black", bold=True))
                            if item_ref.level == 1:
                                Item_refs_location.objects.get_or_create(child=item_ref.child, location_id=location.id, parent_id=parent_id)
                                # Item_refs_location.objects.get_or_create(child=item_refs.child, location_id=location.id, main_item_id=_data.main_item_id, parent_id=parent_id)
                            else:
                                Item_refs_location.objects.get_or_create(child=item_ref.child, parent=item_ref.parent, location_id=location.id, )
                                # Item_refs_location.objects.get_or_create(child=item_refs.child, parent=item_refs.parent, location_id=location.id, main_item_id=_data.main_item_id)

                            if progress.step() != 0:
                                settings.LOCKS.release(key)
                                raise ProgressDroped(progress_deleted)

                Item_refs_location_viewManager.fullRows()
            elif mode == 'move':
                for dropRecord in map(lambda dropRecord: RecordWrapper(**dropRecord), _data.dropRecords):
                    updated = Item_refs_location.objects.filter(child_id=dropRecord.child_id, parent_id=dropRecord.parent_id).update(parent_id=parent_id)
                    logger.debug(f'updated: {updated}')

                Item_refs_location_viewManager.fullRows()
            elif mode == 'copy':
                for dropRecord in map(lambda dropRecord: RecordWrapper(**dropRecord), _data.dropRecords):
                    dropRecord_dict = model_2_dict(dropRecord)
                    delAttr(dropRecord_dict, 'child_id')
                    delAttr(dropRecord_dict, 'parent_id')

                    updated = Item_refs_location.objects.get_or_create(child_id=dropRecord.child_id, parent_id=parent_id, defaults=dropRecord_dict)
                    logger.debug(f'updated: {updated}')

                Item_refs_location_viewManager.fullRows()
            elif mode is None:
                used = _data.used
                props = _data.props
                id = _data.id
                child_id = _data.child_id
                parent_id = _data.parent_id

                if used is False:
                    props &= ~Item_refs_location.props.used
                else:
                    props |= Item_refs_location.props.used

                for item_refs in Item_refs_location.objects1.get_descendants(id=child_id, include_self=True):
                    super().filter(id=item_refs.id).update(props=props)
                    Item_refs_location_viewManager.refreshRows(item_refs.id)

                if used is True and parent_id is not None:
                    for item_refs in Item_refs_location.objects1.get_parents(id=parent_id, include_self=False):
                        super().filter(id=item_refs.id).update(props=props)
                        Item_refs_location_viewManager.refreshRows(item_refs.id)


            if key is not None:
                settings.LOCKS.release(key)

        return data

    def deleteFromRequest(self, request, removed=None, ):
        request = DSRequest(request=request)
        res = 0
        tuple_ids = request.get_olds_tuple_ids()
        with transaction.atomic():
            for id, mode in tuple_ids:
                if mode == 'hide':
                    super().filter(id=id).soft_delete()
                    res += 1
                elif mode == 'visible':
                    super().filter(id=id).soft_restore()
                else:
                    for item_ref in Item_refs_location.objects1.get_descendants(
                            id=Item_refs_location.objects.get(id=id).child.id,
                            order_by_clause='order by level desc'):
                        qty, _ = super().filter(id=item_ref.id).delete()
                        res += qty
        return res

# Не используется !!!!!!!
class Item_refs_location(AuditModel):
    child = ForeignKeyProtect(Item, related_name='Item_refs_location_child')
    location = ForeignKeyProtect(Locations)
    parent = ForeignKeyProtect(Item, related_name='Item_refs_location_parent', blank=True, null=True)
    props = Item_refs_locationManager.props()

    objects = Item_refs_locationManager()
    objects1 = TreeAuditModelManager()

    def __str__(self):
        return f'\n\nID={self.id}, ' \
               f'\nchild=[{self.child}], ' \
               f'\nparent=[{self.parent}], ' \
               f'\nlocation=[{self.location}] '
               # f'\nchild_operation_id={self.child_operation_id}, ' \
               # f'\nparent_operation_id={self.parent_operation_id}'

    class Meta:
        verbose_name = 'Item_refs_location'
        constraints = [
            CheckConstraint(check=~Q(child=F('parent')), name='Item_refs_location_not_circulate_refs'),
            UniqueConstraint(fields=['child_id'], condition=Q(parent_id=None), name='Item_refs_location_unique_constraint_0'),
            UniqueConstraint(fields=['child_id', 'parent_id'], name='Item_refs_location_unique_constraint_1'),
        ]
