import logging

from bitfield import BitField, BitHandler
from django import db
from django.conf import settings
from django.db import transaction, connection
from django.db.models import PositiveIntegerField, BigIntegerField, UniqueConstraint, Q, ProtectedError
from django.forms import model_to_dict

from isc_common import setAttr, delAttr
from isc_common.auth.models.user import User
from isc_common.bit import TurnBitOn
from isc_common.common.functions import delete_dbl_spaces
from isc_common.common.mat_views import refresh_mat_view
from isc_common.fields.related import ForeignKeyProtect
from isc_common.http.DSRequest import DSRequest
from isc_common.managers.common_managet_with_lookup_fields import CommonManagetWithLookUpFieldsManager, CommonManagetWithLookUpFieldsQuerySet
from isc_common.models.audit import AuditModel
from isc_common.progress import managed_progress, ProgressDroped, progress_deleted
from isc_common.string import get_NoneStr
from kaf_pas.ckk.models import get_operations_from_trunsaction
from kaf_pas.kd.models.document_attributes import Document_attributes, Document_attributesManager
from kaf_pas.kd.models.documents import Documents
from kaf_pas.kd.models.lotsman_documents_hierarcy import Lotsman_documents_hierarcy

logger = logging.getLogger(__name__)


class ItemQuerySet(CommonManagetWithLookUpFieldsQuerySet):

    def create(self, **kwargs):
        from kaf_pas.ckk.models.item_history import Item_history

        with transaction.atomic():
            delAttr(kwargs, 'used')

            res = super().create(**kwargs)

            delAttr(kwargs, 'id')
            delAttr(kwargs, 'creator')
            delAttr(kwargs, 'parent_id')
            setAttr(kwargs, 'hcreator', res.creator)
            setAttr(kwargs, 'item', res)
            Item_history.objects.get_or_create(**kwargs)
            return res

    def update(self, **kwargs):
        from kaf_pas.ckk.models.item_history import Item_history

        with transaction.atomic():
            delAttr(kwargs, 'used')
            creator_id = kwargs.get('creator_id')
            if creator_id is None:
                creator_id = self[0].creator.id
                setAttr(kwargs, 'creator_id', creator_id)

            res = super().update(**kwargs)

            item_id = self[0].id
            delAttr(kwargs, 'id')
            delAttr(kwargs, 'creator')
            delAttr(kwargs, 'used')
            setAttr(kwargs, 'hcreator_id', kwargs.get('creator_id'))
            delAttr(kwargs, 'creator_id')
            delAttr(kwargs, 'parent_id')
            setAttr(kwargs, 'item_id', item_id)
            Item_history.objects.get_or_create(**kwargs)
            return res


class ItemManager(CommonManagetWithLookUpFieldsManager):

    @classmethod
    def check_along_items(cls):
        from kaf_pas.production.models import p_id
        from kaf_pas.ckk.models.item_refs import Item_refs
        sql_str = '''select id
                    from ckk_item
                    where id not in (select child_id from ckk_item_refs)'''

        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute(sql_str)
                rows = cursor.fetchall()

                for row, in rows:
                    Item_refs.objects.get_or_create(parent_id=p_id, child_id=row)


    def createFromRequest(self, request):
        from kaf_pas.ckk.models.item_refs import Item_refs
        from kaf_pas.production.models import p_id

        request = DSRequest(request=request)
        data = request.get_data()
        _data = data.copy()

        parent_id = _data.get('id')
        if parent_id is None:
            parent_id = p_id

        delAttr(_data, 'parent')
        delAttr(_data, 'parent_id')
        delAttr(_data, 'id')
        delAttr(_data, 'STMP_1__value_str')
        delAttr(_data, 'STMP_2__value_str')

        props = 0

        props |= Item.props.relevant
        props |= Item.props.man_input
        props |= Item.props.confirmed

        delAttr(_data, 'relevant')
        delAttr(_data, 'where_from')
        delAttr(_data, 'confirmed')
        delAttr(_data, 'used')
        setAttr(_data, 'props', props)
        setAttr(_data, 'creator', request.user)

        # 'STMP_1', 'STMP_2', 'lotsman_document_id', 'lotsman_type_id', 'props', 'version'
        res, created = super().get_or_create(**_data)

        if created:
            logger.debug(f'Added: {res}')

        if parent_id is not None and created is True:
            item_refs, create = Item_refs.objects.get_or_create(parent_id=parent_id, child=res)
            if create:
                logger.debug(f'Added item_ref: {item_refs}')

        res = model_to_dict(res)

        props = res.get('props')
        if props and isinstance(props, BitHandler):
            props = res.get('props')._value
            setAttr(res, 'props', props)
        setAttr(res, 'isFolder', False)
        data.update(res)
        return data

    @classmethod
    def find_item(cls, item):
        if isinstance(item, int):
            item = Item.objects.get(id=item)
        elif not isinstance(item, Item):
            raise Exception('item must be Item or int')

        STMP_2 = item.STMP_2.value_str if item.STMP_2 else None
        STMP_1 = item.STMP_1.value_str if item.STMP_1 else None

        if STMP_2 is None:
            item_query = Item.objects.filter(STMP_1__value_str__delete_dbl_spaces=delete_dbl_spaces(STMP_1))
        elif STMP_1 is None:
            item_query = Item.objects.filter(STMP_2__value_str__delete_dbl_spaces=delete_dbl_spaces(STMP_2))
        else:
            item_query = Item.objects.filter(STMP_1__value_str__delete_dbl_spaces=delete_dbl_spaces(STMP_1), STMP_2__value_str__delete_dbl_spaces=delete_dbl_spaces(STMP_2))

        return [item for item in item_query]

    @classmethod
    def find_item_contains(cls, item):
        if isinstance(item, int):
            item = Item.objects.get(id=item)
        elif not isinstance(item, Item):
            raise Exception('item must be Item or int')

        STMP_2 = item.STMP_2.value_str if item.STMP_2 else None
        STMP_1 = item.STMP_1.value_str if item.STMP_1 else None

        if STMP_2 is None:
            item_query = Item.objects.filter(STMP_1__value_str__delete_dbl_spaces__contains=delete_dbl_spaces(STMP_1))
        elif STMP_1 is None:
            item_query = Item.objects.filter(STMP_2__value_str__delete_dbl_spaces__contains=delete_dbl_spaces(STMP_2))
        else:
            item_query = Item.objects.filter(STMP_1__value_str__delete_dbl_spaces__contains=delete_dbl_spaces(STMP_1), STMP_2__value_str__delete_dbl_spaces__contains=delete_dbl_spaces(STMP_2))

        return [item for item in item_query]

    @classmethod
    def find_item1(cls, **kwargs):
        STMP_1 = kwargs.get('STMP_1')
        STMP_2 = kwargs.get('STMP_2')

        if STMP_2 is None:
            item_query = Item.objects.filter(STMP_1__value_str__delete_dbl_spaces=delete_dbl_spaces(STMP_1))
        elif STMP_1 is None:
            item_query = Item.objects.filter(STMP_2__value_str__delete_dbl_spaces=delete_dbl_spaces(STMP_2))
        else:
            item_query = Item.objects.filter(STMP_1__value_str__delete_dbl_spaces=delete_dbl_spaces(STMP_1), STMP_2__value_str__delete_dbl_spaces=delete_dbl_spaces(STMP_2))

        return [item for item in item_query]

    @classmethod
    def find_item1_contains(cls, **kwargs):
        STMP_1 = kwargs.get('STMP_1')
        STMP_2 = kwargs.get('STMP_2')
        deleted_at = kwargs.get('deleted_at')

        if STMP_2 is None and STMP_1 is not None:
            if deleted_at is None:
                item_query = Item.objects.filter(STMP_1__value_str__delete_dbl_spaces__contains=delete_dbl_spaces(STMP_1), deleted_at=None)
            else:
                item_query = Item.objects.filter(STMP_1__value_str__delete_dbl_spaces__contains=delete_dbl_spaces(STMP_1))
        elif STMP_1 is None and STMP_2 is not None:
            if deleted_at is None:
                item_query = Item.objects.filter(STMP_2__value_str__delete_dbl_spaces__contains=delete_dbl_spaces(STMP_2), deleted_at=None)
            else:
                item_query = Item.objects.filter(STMP_2__value_str__delete_dbl_spaces__contains=delete_dbl_spaces(STMP_2))
        elif STMP_1 is not None and STMP_2 is not None:
            if deleted_at is None:
                item_query = Item.objects.filter(STMP_1__value_str__delete_dbl_spaces__contains=delete_dbl_spaces(STMP_1), STMP_2__value_str__delete_dbl_spaces__contains=delete_dbl_spaces(STMP_2), deleted_at=None)
            else:
                item_query = Item.objects.filter(STMP_1__value_str__delete_dbl_spaces__contains=delete_dbl_spaces(STMP_1), STMP_2__value_str__delete_dbl_spaces__contains=delete_dbl_spaces(STMP_2))
        else:
            return []

        return [item for item in item_query]

    @classmethod
    def check_4_production(cls, item):
        if isinstance(item, int):
            id = item
        elif isinstance(item, Item):
            id = item.id
        else:
            raise Exception('item must be Item or int')

        with connection.cursor() as cursor:
            cursor.execute('''select count(*) from ckk_item_not_typed_top_level_view
                                where parent_id = %s or child_id = %s''', [id, id])
            qty, = cursor.fetchone()
            if qty == 0:
                cursor.execute('''select count(*) from ckk_item_typed_top_level_view
                                    where parent_id = %s or child_id = %s''', [id, id])
                qty, = cursor.fetchone()
            return qty > 0

    @classmethod
    def delete_recursive(cls, item_id, delete_lines=False, soft_delete=None, user=None, props=TurnBitOn(0, 0), document=None, show_progress=True):
        from kaf_pas.ckk.models.item_document import Item_document
        from kaf_pas.ckk.models.item_history import Item_history
        from kaf_pas.ckk.models.item_image_refs import Item_image_refs
        from kaf_pas.ckk.models.item_line import Item_line
        from kaf_pas.ckk.models.item_refs import Item_refs
        from kaf_pas.production.models.operations_item import Operations_item
        from kaf_pas.ckk.models.item_varians import Item_varians

        key = 'ItemManager.delete_recursive'
        settings.LOCKS.acquire(key)
        item_lotsman_document_cnt = 0
        if document is not None:
            if ItemManager.check_4_production(item=item_id) == True:
                settings.LOCKS.release(key)
                return 2

        sql_text = None
        if isinstance(document, Documents):
            sql_text = f'''WITH RECURSIVE r AS (
                                                    SELECT cir.*, 1 AS level
                                                    FROM ckk_item_refs cir
                                                             join ckk_item cich on cich.id = cir.child_id
                                                    WHERE cir.child_id IN ({item_id})
                                                        and cich.document_id = {document.id}

                                                    union all

                                                    SELECT cir.*, r.level + 1 AS level
                                                    FROM ckk_item_refs cir
                                                        join ckk_item cich on cich.id = cir.child_id
                                                        JOIN r ON cir.parent_id = r.child_id
                                                    WHERE cich.document_id = {document.id}
                                                )
                                                select * from r'''
        elif isinstance(document, Lotsman_documents_hierarcy):
            sql_text = f'''WITH RECURSIVE r AS (
                                                    SELECT cir.*, 1 AS level
                                                    FROM ckk_item_refs cir
                                                             join ckk_item cich on cich.id = cir.child_id
                                                    WHERE cir.child_id IN ({item_id})
                                                      and cich.lotsman_document_id = {document.id}

                                                    union all

                                                    SELECT cir.*, r.level + 1 AS level
                                                    FROM ckk_item_refs cir
                                                             join ckk_item cich on cich.id = cir.child_id
                                                             JOIN r ON cir.parent_id = r.child_id
                                                    WHERE cich.lotsman_document_id = {document.id}
                                                )
                                                select * from r'''

        cnt = Item_refs.objects.get_descendants_count(id=item_id, sql_text=sql_text)

        def _delete(progress=None):
            try:
                with transaction.atomic():
                    try:
                        item = Item.objects.get(id=item_id)
                        if cnt == 1:
                            Item_refs.objects1.filter(parent=item).delete_with_checked()
                            Item_refs.objects1.filter(child=item).delete_with_checked()
                            Item_line.objects.filter(parent=item).delete()
                            Item_line.objects.filter(child=item).delete()
                            Item_history.objects.filter(item=item).delete()
                            Item_varians.objects.filter(parent=item).delete()
                            Item_varians.objects.filter(child=item).delete()
                            item.delete()
                        else:
                            if progress is not None:
                                progress.setContentsLabel(f'''<h3>Удаление товарной позиции ({item.STMP_1.value_str if item.STMP_1 else ''} : {item.STMP_2.value_str if item.STMP_2 else ''}).</h3>''')

                            # 3572269
                            for item in Item_refs.objects.get_descendants(id=item_id, order_by_clause='order by level desc', sql_text=sql_text):
                                _continue = False
                                if soft_delete is None:
                                    if document is not None:
                                        if ItemManager.check_4_production(item=item.child_id) == True:
                                            _continue = True

                                    if _continue:
                                        _continue = False
                                        continue

                                    Item_varians.objects.filter(parent=item.parent, child=item.child).delete()

                                    Item_image_refs.objects.filter(item_id=item.child_id).delete()

                                    if delete_lines:
                                        Item_line.objects.filter(parent_id=item.child_id).delete()
                                        Item_line.objects.filter(child_id=item.child_id).delete()

                                    Item_refs.objects1.filter(parent_id=item.child_id).delete_with_checked()
                                    Item_refs.objects1.filter(child_id=item.child_id).delete_with_checked()

                                    Operations_item.objects.filter(item=item.child_id).delete()
                                    # Ready_2_launch_detail.objects.filter(item=item.child_id).delete()

                                    Item_document.objects.filter(item_id=item.child_id).delete()

                                    Item_history.objects.filter(item=item.child).delete()
                                    Item.objects.filter(id=item.child_id).delete()
                                else:
                                    if soft_delete == 'hide':
                                        Item.objects.filter(id=item.child_id).soft_delete()
                                    elif soft_delete == 'visible':
                                        Item.objects.filter(id=item.child_id).soft_restore()
                                    else:
                                        raise Exception(f'soft_delete : {soft_delete} this unknown mode')

                                if progress is not None:
                                    if progress.step() != 0:
                                        settings.LOCKS.release(key)
                                        raise ProgressDroped(progress_deleted)
                    except Item.DoesNotExist:
                        settings.LOCKS.release(key)

            except db.models.deletion.ProtectedError as ex:
                logger.error(f'Item_refs: {item}')
                settings.LOCKS.release(key)
                raise ex

        if show_progress and cnt > 0:
            with managed_progress(
                    id=f'delete_recursive_{item_id}',
                    qty=cnt,
                    user=user,
                    message='Удаление товарной(ых) позиций',
                    title='Выполнено',
                    props=props
            ) as progress:
                _delete(progress)
        else:
            _delete()

        settings.LOCKS.release(key)

        if item_lotsman_document_cnt > 0:
            refresh_mat_view('kd_lotsman_documents_hierarcy_mview')

    @classmethod
    def rec(cls, data):
        _data = data.copy()
        relevant = data.get('relevant')
        confirmed = data.get('confirmed')
        props = data.get('props')

        if relevant == 'Актуален':
            props |= Item.props.relevant
        else:
            props &= ~Item.props.relevant

        if confirmed == 'Подтвержден':
            props |= Item.props.confirmed
        else:
            props &= ~Item.props.confirmed

        where_from = data.get('where_from')
        if where_from == 'Получено из чертежа':
            props |= Item.props.from_cdw
        elif where_from == 'Получено из спецификации':
            props |= Item.props.from_spw
        elif where_from == 'Получено из бумажного архива':
            props |= Item.props.from_pdf
        elif where_from == 'Занесено вручную':
            props |= Item.props.man_input

        delAttr(data, 'relevant')
        delAttr(data, 'confirmed')
        delAttr(data, 'where_from')
        delAttr(data, 'qty_operations')
        delAttr(data, 'refs_props')
        delAttr(data, 'icon')
        delAttr(data, 'id')
        delAttr(data, 'STMP_1__value_str')
        delAttr(data, 'STMP_2__value_str')
        delAttr(data, 'document__file_document')
        delAttr(data, 'isFolder')
        delAttr(data, 'isLotsman')
        delAttr(data, 'parent_id')
        delAttr(data, 'section')
        delAttr(data, 'used')

        setAttr(data, 'props', props)

        version = ItemManager.get_verstion(
            STMP_1=data.get('STMP_1_id'),
            STMP_2=data.get('STMP_2_id'),
            props=data.get('props')
        )

        if version != data.get('version'):
            setAttr(data, 'version', version)

        return _data

    @classmethod
    def replaceItems(cls, dropRecords, targetRecord, func_after=None):
        from kaf_pas.ckk.models.item_refs import Item_refs
        from kaf_pas.ckk.models.item_line import Item_line

        res = 0
        for dropRecord in dropRecords:
            item_refs, created = Item_refs.objects.get_or_create(parent_id=targetRecord.get('parent_id'), child_id=dropRecord.get('id'))
            if not created:
                item_refs.soft_restore()

            res += 1

            item_line = model_to_dict(Item_line.objects.get(parent_id=targetRecord.get('parent_id'), child_id=targetRecord.get('id')))

            delAttr(item_line, 'id')
            delAttr(item_line, 'parent')
            delAttr(item_line, 'child')
            setAttr(item_line, 'SPC_CLM_NAME_id', dropRecord.get('STMP_1_id'))
            delAttr(item_line, 'SPC_CLM_NAME')
            setAttr(item_line, 'SPC_CLM_MARK_id', dropRecord.get('STMP_2_id'))
            delAttr(item_line, 'SPC_CLM_MARK')
            setAttr(item_line, 'SPC_CLM_FORMAT_id', item_line.get('SPC_CLM_FORMAT'))
            delAttr(item_line, 'SPC_CLM_FORMAT')
            setAttr(item_line, 'SPC_CLM_ZONE_id', item_line.get('SPC_CLM_ZONE'))
            delAttr(item_line, 'SPC_CLM_ZONE')
            setAttr(item_line, 'SPC_CLM_POS_id', item_line.get('SPC_CLM_POS'))
            delAttr(item_line, 'SPC_CLM_POS')
            setAttr(item_line, 'SPC_CLM_COUNT_id', item_line.get('SPC_CLM_COUNT'))
            delAttr(item_line, 'SPC_CLM_COUNT')
            setAttr(item_line, 'SPC_CLM_NOTE_id', item_line.get('SPC_CLM_NOTE'))
            delAttr(item_line, 'SPC_CLM_NOTE')
            setAttr(item_line, 'SPC_CLM_MASSA_id', item_line.get('SPC_CLM_MASSA'))
            delAttr(item_line, 'SPC_CLM_MASSA')
            setAttr(item_line, 'SPC_CLM_MATERIAL_id', item_line.get('SPC_CLM_MATERIAL'))
            delAttr(item_line, 'SPC_CLM_MATERIAL')
            setAttr(item_line, 'SPC_CLM_USER_id', item_line.get('SPC_CLM_USER'))
            delAttr(item_line, 'SPC_CLM_USER')
            setAttr(item_line, 'SPC_CLM_KOD_id', item_line.get('SPC_CLM_KOD'))
            delAttr(item_line, 'SPC_CLM_KOD')
            setAttr(item_line, 'SPC_CLM_FACTORY_id', item_line.get('SPC_CLM_FACTORY'))
            delAttr(item_line, 'SPC_CLM_FACTORY')

            item_line, created = Item_line.objects.get_or_create(
                parent_id=targetRecord.get('parent_id'),
                child_id=dropRecord.get('id'),
                defaults=item_line
            )
            if not created:
                item_line.soft_restore()
            res += 1

            try:
                Item_refs.objects1.filter(parent_id=targetRecord.get('parent_id'), child_id=targetRecord.get('id')).delete_with_checked()
            except ProtectedError:
                Item_refs.objects1.filter(parent_id=targetRecord.get('parent_id'), child_id=targetRecord.get('id')).soft_delete()

            try:
                Item_line.objects.filter(parent_id=targetRecord.get('parent_id'), child_id=targetRecord.get('id')).delete()
            except ProtectedError:
                Item_line.objects.filter(parent_id=targetRecord.get('parent_id'), child_id=targetRecord.get('id')).soft_delete()

            if callable(func_after):
                func_after(dropRecord, targetRecord)

        return res

    def updateFromRequest(self, request, removed=None, function=None):
        from kaf_pas.ckk.models.item_refs import Item_refs
        from kaf_pas.ckk.models.item_line import Item_line

        request = DSRequest(request=request)
        data = request.get_data()

        with transaction.atomic():
            targetRecord = data.get('targetRecord')
            dropRecords = data.get('dropRecords')
            if data.get('mode') == 'move':
                res = 0
                for dropRecord in dropRecords:
                    res += Item_refs.objects.filter(parent_id=dropRecord.get('parent_id'), child_id=dropRecord.get('id')).update(parent_id=targetRecord.get('id'))
                    res += Item_line.objects.filter(parent_id=dropRecord.get('parent_id'), child_id=dropRecord.get('id')).update(parent_id=targetRecord.get('id'))
                return res
            elif data.get('mode') == 'copy':
                res = 0
                for dropRecord in dropRecords:
                    Item_refs.objects.create(parent_id=targetRecord.get('id'), child_id=dropRecord.get('id'))
                    res += 1
                return res
            elif data.get('mode') == 'replace':
                return ItemManager.replaceItems(dropRecords=dropRecords, targetRecord=targetRecord)
            else:
                # res = []
                _data = ItemManager.rec(data.copy())

                props = _data.get('props')
                if _data.get('confirmed') == 'Подтвержден':
                    props |= Item.props.confirmed
                elif _data.get('confirmed') == 'Не подтвержден':
                    props &= ~Item.props.confirmed

                if _data.get('relevant') == 'Актуален':
                    props |= Item.props.relevant
                elif _data.get('relevant') == 'Не актуален':
                    props &= ~Item.props.relevant

                update_dict = dict(
                    STMP_1_id=_data.get('STMP_1_id'),
                    STMP_2_id=_data.get('STMP_2_id'),
                    version=_data.get('version'),
                    document_id=_data.get('document_id'),
                    lotsman_document_id=_data.get('lotsman_document_id'),
                    lotsman_type_id=_data.get('lotsman_type_id'),
                    creator_id=_data.get('creator_id'),
                    props=props
                )
                Item.objects.filter(id=_data.get('id')).update(**update_dict)

                refs_props = _data.get('refs_props')
                if refs_props is not None:
                    refs_id = _data.get('refs_id')

                    if _data.get('used') == True:
                        refs_props |= Item_refs.props.used
                    elif _data.get('used') == False:
                        refs_props &= ~Item_refs.props.used

                    refs_data = dict()
                    setAttr(refs_data, 'props', refs_props)

                    Item_refs.objects.filter(id=refs_id).update(**refs_data)

                return _data

    def replaceFromRequest(self, request):

        request = DSRequest(request=request)
        data = request.get_data()

        def func_after(dropRecord, targetRecord):
            from kaf_pas.ckk.models.item_varians import Item_varians
            from kaf_pas.ckk.models.item_view import Item_viewManager

            for item_varians in Item_varians.objects.filter(
                    parent_id=targetRecord.get('parent_id'),
                    child_id=targetRecord.get('id'),
                    refs_props=targetRecord.get('refs_props')):
                item_varians.child_id = dropRecord.get('id')
                item_varians.save()

            # Item_viewManager.fullRows()
            Item_viewManager.refreshRows(dict(
                id=dropRecord.get('id'),
                parent_id=targetRecord.get('parent_id')
            ))

        with transaction.atomic():
            targetRecord = data.get('targetRecord')
            dropRecords = data.get('dropRecords')
            dropRecords = map(lambda x: dict(id=x.get('item_id'), STMP_1_id=x.get('STMP_1_id'), STMP_2_id=x.get('STMP_2_id')), dropRecords)
            res = ItemManager.replaceItems(dropRecords=dropRecords, targetRecord=targetRecord, func_after=func_after)
            return res

    def deleteFromRequest(self, request, removed=None, ):
        from kaf_pas.ckk.models.item_refs import Item_refs
        from kaf_pas.ckk.models.item_line import Item_line

        request = DSRequest(request=request)
        data = request.get_data()
        res = 0

        mode = None
        key = 'ItemManager.deleteFromRequest'
        with transaction.atomic():
            operations = get_operations_from_trunsaction(data)
            if isinstance(operations, list):
                for operation in get_operations_from_trunsaction(data):
                    settings.LOCKS.acquire(key)
                    _data = operation.get('data')
                    if _data.get('mode') == 'deleteInner':
                        mode = 'deleteInner'
                        records = _data.get('records')

                        if isinstance(records, list):
                            for record in records:
                                res, _ = Item_refs.objects1.filter(child_id=record.get('id'), parent_id=record.get('parent_id')).delete_with_checked()
                                res, _ = Item_line.objects.filter(child_id=record.get('id'), parent_id=record.get('parent_id')).delete()
                    settings.LOCKS.release(key)

                if mode == 'deleteInner':
                    return res
            elif isinstance(data, dict):
                if data.get('mode') == 'deleteInner':
                    settings.LOCKS.acquire(key)
                    records = data.get('records')

                    if isinstance(records, list):
                        for record in records:
                            if record.get('parent_id') is None:
                                res, _ = Item_refs.objects1.filter(child_id=record.get('id'), parent__isnull=True).delete_with_checked()
                                res, _ = Item_line.objects.filter(child_id=record.get('id'), parent__isnull=True).delete()
                            else:
                                res, _ = Item_refs.objects1.filter(child_id=record.get('id'), parent_id=record.get('parent_id')).delete_with_checked()
                                res, _ = Item_line.objects.filter(child_id=record.get('id'), parent_id=record.get('parent_id')).delete()
                        settings.LOCKS.release(key)
                        return res
                    settings.LOCKS.release(key)
                elif data.get('mode') == 'reloadRefs':
                    records = data.get('records')
                    res = 0
                    if isinstance(records, list):
                        settings.LOCKS.acquire(key)
                        for record in records:
                            id = record.get('id')

                            for item_line in Item_line.objects.filter(parent_id=id):
                                item_refs, _ = Item_refs.objects.get_or_create(parent_id=id, child=item_line.child)
                                res += 1
                        settings.LOCKS.release(key)

                    settings.LOCKS.release(key)
                    return res

        for id, mode in request.get_tuple_ids():
            if mode in ['hide', 'visible']:
                res = self.delete_recursive(item_id=id, soft_delete=mode, delete_lines=True, user=request.user_id)
            else:
                res = self.delete_recursive(item_id=id, delete_lines=True, user=request.user_id)
        return res

    def lookupFromRequest(self, request):
        request = DSRequest(request=request)
        data = request.get_data()

        attr_type__code = data.get('attr_type__code')
        value_str = data.get(f'{attr_type__code}__value_str')
        value_int = data.get(f'{attr_type__code}__value_int')

        if value_str is None and value_int is not None:
            value_str = str(value_int)

        if value_str is None:
            return None

        res, created = Document_attributesManager.get_or_create_attribute(attr_codes=attr_type__code, value_str=value_str)
        res = model_to_dict(res)
        if res.get('value_str') == 'null':
            setAttr(res, 'value_str', None)
        return res

    @classmethod
    def get_verstion(cls, STMP_1, STMP_2, props, version=None, inc=1):
        key = 'ItemManager.get_verstion'
        settings.LOCKS.acquire(key)

        if isinstance(STMP_1, int):
            STMP_1 = Document_attributes.objects.get(id=STMP_1)

        if isinstance(STMP_2, int):
            STMP_2 = Document_attributes.objects.get(id=STMP_2)

        while True:
            query = Item.objects.filter(
                STMP_1=STMP_1,
                STMP_2=STMP_2,
                props=props,
                version=version
            )

            if query.count() == 0:
                settings.LOCKS.release(key)
                return version
            else:
                version = query.order_by('-version')[0].version
                if version is None:
                    version = 1
                else:
                    version += inc
                logger.debug(f'version: {version}')

    @classmethod
    def getRecord(cls, record):
        res = {
            'id': record.id,
            'STMP_1_id': record.STMP_1.id if record.STMP_1 else None,
            'STMP_1__value_str': record.STMP_1.value_str if record.STMP_1 else None,
            'STMP_2_id': record.STMP_2.id if record.STMP_2 else None,
            'STMP_2__value_str': record.STMP_2.value_str if record.STMP_2 else None,
            'lastmodified': record.lastmodified,
            'item_name': record.item_name,
            'version': record.version,
            'document_id': record.document.id if record.document else None,
            'document__file_document': record.document.file_document if record.document else None,
            'editing': record.editing,
            'deliting': record.deliting,
        }
        return res

    def get_queryset(self):
        return ItemQuerySet(self.model, using=self._db)

    def checkRecursives(self, request):
        from kaf_pas.ckk.management.commands.check_item_cicular_refs import check_level
        from isc_common.models.deleted_progresses import Deleted_progresses

        request = DSRequest(request=request)
        data = request.get_data()
        if isinstance(data, dict) and isinstance(data.get('records'), list):
            cycle_ref = []
            with managed_progress(
                    id=f'''checkRecursives_{request.user.id}''',
                    qty=1000,
                    user=request.user,
                    message='<h3>Поиск циклических зависемостей.</h3>',
                    title='Выполнено',
                    props=TurnBitOn(0, 0)
            ) as progress:
                try:
                    for record in data.get('records'):
                        cycle_ref.extend(check_level(parent_array=list(), item=Item.objects.get(id=record.get('id')), level=1, table='Item_refs', progress=progress))
                    if len(cycle_ref) == 0:
                        progress.sendInfo('Циклических зависемостей не найдено.')
                    else:
                        progress.sendInfo('\n'.join(cycle_ref))
                    return dict(messages=cycle_ref)
                except ProgressDroped as ex:
                    Deleted_progresses.objects.filter(id_progress=progress.id, user=progress.user).delete()
                    raise ex
        raise Exception('Not data.')

    @classmethod
    def _getQtyChilds(cls, records):
        from kaf_pas.ckk.models.item_qty import Item_qty

        res = 0
        if isinstance(records, list):
            with connection.cursor() as cursor:
                for record in records:
                    cursor.execute('''WITH RECURSIVE r AS (
                                                                SELECT *, 1 AS level
                                                                FROM ckk_item_refs
                                                                WHERE parent_id IN (%s)
                                                                union all
                                                                SELECT ckk_item_refs.*, r.level + 1 AS level
                                                                FROM ckk_item_refs
                                                                         JOIN r
                                                                              ON ckk_item_refs.parent_id = r.child_id)

                                                            select  count(*)
                                                            from r''', [record.get('id')])
                    qty, = cursor.fetchone()
                    res += qty
                    Item_qty.objects.create(
                        child_id=record.get('id'),
                        parent_id=record.get('parent_id'),
                        qty=qty
                    )
        return dict(qty=res)

    def getQtyChilds(self, request):

        request = DSRequest(request=request)
        data = request.get_data()
        if isinstance(data, dict):
            records = data.get('records')
            if isinstance(records, list):
                return ItemManager._getQtyChilds(records=records)

    def getGrouping(self, request):

        request = DSRequest(request=request)
        data = request.get_data()
        if isinstance(data, dict):
            records = data.get('records')
            if isinstance(records, list):
                return ItemManager._getQtyChilds(records=records)


class Item_add:
    @classmethod
    def get_prop_field(cls):
        return BitField(flags=(
            ('relevant', 'Актуальность'),  # 1
            ('from_cdw', 'Получено из чертежа'),  # 2
            ('from_spw', 'Получено из спецификации'),  # 4
            ('for_line', 'Строка спецификации'),  # 8
            ('from_pdf', 'Получено из бумажного архива'),  # 16
            ('man_input', 'Занесено вручную'),  # 32
            ('copied', 'Скопировано'),  # 64
            ('from_lotsman', 'Получено из Лоцмана'),  # 128
            ('confirmed', 'Подтвержден'),  # 256
        ), default=1, db_index=True)


class Item(AuditModel):
    STMP_1 = ForeignKeyProtect(Document_attributes, verbose_name='Наименование изделия', related_name='STMP_1', null=True, blank=True)
    STMP_2 = ForeignKeyProtect(Document_attributes, verbose_name='Обозначение изделия', related_name='STMP_2', null=True, blank=True)
    version = PositiveIntegerField(null=True, blank=True)

    props = Item_add.get_prop_field()

    document = ForeignKeyProtect(Documents, verbose_name='Документ', null=True, blank=True)
    lotsman_document = ForeignKeyProtect(Lotsman_documents_hierarcy, verbose_name='Документ из Лоцмана', null=True, blank=True)
    lotsman_type_id = BigIntegerField(null=True, blank=True)
    creator = ForeignKeyProtect(User)

    objects = ItemManager()

    @property
    def relevant(self):
        if self.props.relevant:
            return 'Актуален'
        else:
            return 'Актуален'

    @property
    def confirmed(self):
        if self.props.confirmed:
            return 'Подтвержден'
        else:
            return 'Не подтвержден'

    @property
    def where_from(self):
        if self.props.from_cdw:
            return 'Получено из чертежа'
        elif self.props.from_spw:
            return 'Получено из спецификации'
        elif self.props.for_line:
            return 'Строка спецификации'
        elif self.props.from_pdf:
            return 'Получено из бумажного архива'
        elif self.props.man_input:
            return 'Занесено вручную'
        elif self.props.copied:
            return 'Скопировано'
        elif self.props.from_lotsman:
            return 'Получено из Лоцмана'
        else:
            return ''

    @property
    def item_name(self):
        if self.STMP_1 is not None and self.STMP_2 is not None:
            return f'{get_NoneStr(self.STMP_1.value_str)}: {get_NoneStr(self.STMP_2.value_str)}'
        elif self.STMP_1 is None and self.STMP_2 is not None:
            return get_NoneStr(self.STMP_2.value_str)
        elif self.STMP_1 is not None and self.STMP_2 is None:
            return get_NoneStr(self.STMP_1.value_str)
        else:
            return 'Неизвестен'

    @classmethod
    def get_vaslue_str(cls, doc_attr):
        if doc_attr.value_str is None:
            return None
        return doc_attr.value_str.strip() if doc_attr else None

    def __str__(self):
        return f'ID={self.id} STMP_1=[{self.STMP_1}], STMP_2=[{self.STMP_2}], props={self.props}, version={self.version}'

    def __repr__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Товарная позиция'
        constraints = [
            UniqueConstraint(fields=['props'], condition=Q(STMP_1=None) & Q(STMP_2=None) & Q(lotsman_document_id=None) & Q(lotsman_type_id=None) & Q(version=None), name='Item_unique_constraint_0'),
            UniqueConstraint(fields=['STMP_1', 'props'], condition=Q(STMP_2=None) & Q(lotsman_document_id=None) & Q(lotsman_type_id=None) & Q(version=None), name='Item_unique_constraint_1'),
            UniqueConstraint(fields=['STMP_2', 'props'], condition=Q(STMP_1=None) & Q(lotsman_document_id=None) & Q(lotsman_type_id=None) & Q(version=None), name='Item_unique_constraint_2'),
            UniqueConstraint(fields=['STMP_1', 'STMP_2', 'props'], condition=Q(lotsman_document_id=None) & Q(lotsman_type_id=None) & Q(version=None), name='Item_unique_constraint_3'),
            UniqueConstraint(fields=['props', 'version'], condition=Q(STMP_1=None) & Q(STMP_2=None) & Q(lotsman_document_id=None) & Q(lotsman_type_id=None), name='Item_unique_constraint_4'),
            UniqueConstraint(fields=['STMP_1', 'props', 'version'], condition=Q(STMP_2=None) & Q(lotsman_document_id=None) & Q(lotsman_type_id=None), name='Item_unique_constraint_5'),
            UniqueConstraint(fields=['STMP_2', 'props', 'version'], condition=Q(STMP_1=None) & Q(lotsman_document_id=None) & Q(lotsman_type_id=None), name='Item_unique_constraint_6'),
            UniqueConstraint(fields=['STMP_1', 'STMP_2', 'props', 'version'], condition=Q(lotsman_document_id=None) & Q(lotsman_type_id=None), name='Item_unique_constraint_7'),
            UniqueConstraint(fields=['lotsman_document_id', 'props'], condition=Q(STMP_1=None) & Q(STMP_2=None) & Q(lotsman_type_id=None) & Q(version=None), name='Item_unique_constraint_8'),
            UniqueConstraint(fields=['STMP_1', 'lotsman_document_id', 'props'], condition=Q(STMP_2=None) & Q(lotsman_type_id=None) & Q(version=None), name='Item_unique_constraint_9'),
            UniqueConstraint(fields=['STMP_2', 'lotsman_document_id', 'props'], condition=Q(STMP_1=None) & Q(lotsman_type_id=None) & Q(version=None), name='Item_unique_constraint_10'),
            UniqueConstraint(fields=['STMP_1', 'STMP_2', 'lotsman_document_id', 'props'], condition=Q(lotsman_type_id=None) & Q(version=None), name='Item_unique_constraint_11'),
            UniqueConstraint(fields=['lotsman_document_id', 'props', 'version'], condition=Q(STMP_1=None) & Q(STMP_2=None) & Q(lotsman_type_id=None), name='Item_unique_constraint_12'),
            UniqueConstraint(fields=['STMP_1', 'lotsman_document_id', 'props', 'version'], condition=Q(STMP_2=None) & Q(lotsman_type_id=None), name='Item_unique_constraint_13'),
            UniqueConstraint(fields=['STMP_2', 'lotsman_document_id', 'props', 'version'], condition=Q(STMP_1=None) & Q(lotsman_type_id=None), name='Item_unique_constraint_14'),
            UniqueConstraint(fields=['STMP_1', 'STMP_2', 'lotsman_document_id', 'props', 'version'], condition=Q(lotsman_type_id=None), name='Item_unique_constraint_15'),
            UniqueConstraint(fields=['lotsman_type_id', 'props'], condition=Q(STMP_1=None) & Q(STMP_2=None) & Q(lotsman_document_id=None) & Q(version=None), name='Item_unique_constraint_16'),
            UniqueConstraint(fields=['STMP_1', 'lotsman_type_id', 'props'], condition=Q(STMP_2=None) & Q(lotsman_document_id=None) & Q(version=None), name='Item_unique_constraint_17'),
            UniqueConstraint(fields=['STMP_2', 'lotsman_type_id', 'props'], condition=Q(STMP_1=None) & Q(lotsman_document_id=None) & Q(version=None), name='Item_unique_constraint_18'),
            UniqueConstraint(fields=['STMP_1', 'STMP_2', 'lotsman_type_id', 'props'], condition=Q(lotsman_document_id=None) & Q(version=None), name='Item_unique_constraint_19'),
            UniqueConstraint(fields=['lotsman_type_id', 'props', 'version'], condition=Q(STMP_1=None) & Q(STMP_2=None) & Q(lotsman_document_id=None), name='Item_unique_constraint_20'),
            UniqueConstraint(fields=['STMP_1', 'lotsman_type_id', 'props', 'version'], condition=Q(STMP_2=None) & Q(lotsman_document_id=None), name='Item_unique_constraint_21'),
            UniqueConstraint(fields=['STMP_2', 'lotsman_type_id', 'props', 'version'], condition=Q(STMP_1=None) & Q(lotsman_document_id=None), name='Item_unique_constraint_22'),
            UniqueConstraint(fields=['STMP_1', 'STMP_2', 'lotsman_type_id', 'props', 'version'], condition=Q(lotsman_document_id=None), name='Item_unique_constraint_23'),
            UniqueConstraint(fields=['lotsman_document_id', 'lotsman_type_id', 'props'], condition=Q(STMP_1=None) & Q(STMP_2=None) & Q(version=None), name='Item_unique_constraint_24'),
            UniqueConstraint(fields=['STMP_1', 'lotsman_document_id', 'lotsman_type_id', 'props'], condition=Q(STMP_2=None) & Q(version=None), name='Item_unique_constraint_25'),
            UniqueConstraint(fields=['STMP_2', 'lotsman_document_id', 'lotsman_type_id', 'props'], condition=Q(STMP_1=None) & Q(version=None), name='Item_unique_constraint_26'),
            UniqueConstraint(fields=['STMP_1', 'STMP_2', 'lotsman_document_id', 'lotsman_type_id', 'props'], condition=Q(version=None), name='Item_unique_constraint_27'),
            UniqueConstraint(fields=['lotsman_document_id', 'lotsman_type_id', 'props', 'version'], condition=Q(STMP_1=None) & Q(STMP_2=None), name='Item_unique_constraint_28'),
            UniqueConstraint(fields=['STMP_1', 'lotsman_document_id', 'lotsman_type_id', 'props', 'version'], condition=Q(STMP_2=None), name='Item_unique_constraint_29'),
            UniqueConstraint(fields=['STMP_2', 'lotsman_document_id', 'lotsman_type_id', 'props', 'version'], condition=Q(STMP_1=None), name='Item_unique_constraint_30'),
            UniqueConstraint(fields=['STMP_1', 'STMP_2', 'lotsman_document_id', 'lotsman_type_id', 'props', 'version'], name='Item_unique_constraint_31'),
        ]
        db_constraints = {
            'Item_not_null_STMP1_STMP2': 'CHECK ("STMP_1_id" IS NOT NULL OR "STMP_2_id" IS NOT NULL)',
        }
