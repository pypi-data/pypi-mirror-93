import logging

from django.db import connection, transaction

from isc_common import Stack
from isc_common.bit import TurnBitOn
from isc_common.common.mat_views import create_tmp_mat_view, drop_mat_view
from isc_common.logger.Logger import Logger
from isc_common.progress import managed_progress, ProgressDroped, progress_deleted

logger = logging.getLogger(__name__)
logger.__class__ = Logger


class Lotsman_documents_hierarcyManagerExt:
    def __init__(self, user, logger=logger, documentManagerExt=None):
        self.user = user
        self.documentManagerExt = documentManagerExt
        self.logger = logger

    def make_items(self, lotsman_documents_hierarcy_view_record):
        from kaf_pas.ckk.models.item import Item
        from kaf_pas.ckk.models.item_refs import Item_refs
        from kaf_pas.kd.models.document_attributes import Document_attributesManager
        from kaf_pas.kd.models.lotsman_documents_hierarcy import Lotsman_documents_hierarcy
        from kaf_pas.kd.models.lotsman_documents_hierarcy_view import Lotsman_documents_hierarcy_view
        from kaf_pas.system.models.contants import Contants
        # from kaf_pas.ckk.models.tmp_item_refs import Tmp_Item_refsManager

        items_pairs = Stack()

        mat_view_name = None
        try:
            imp_frpm_lotsman_label = 'Импорт из Лоцмана'

            top_item, created = Item.objects.get_or_create(
                STMP_1=Document_attributesManager.get_or_create_attribute(
                    attr_codes='STMP_1',
                    value_str=imp_frpm_lotsman_label,
                    logger=self.logger
                )[0],
                props=Item.props.relevant | Item.props.from_lotsman
            )

            item_refs, _ = Item_refs.objects.get_or_create(child=top_item)
            if item_refs.parent is not None:
                item_refs.delete()
                item_refs, _ = Item_refs.objects.get_or_create(child=top_item)

            item_top_level, _ = Contants.objects.update_or_create(
                code='top_level',
                defaults=dict(
                    name='Вершины товарных позиций')
            )
            const4, _ = Contants.objects.update_or_create(
                code='lotsman_top_level',
                defaults=dict(
                    parent=item_top_level,
                    name=imp_frpm_lotsman_label,
                    value=top_item.id)
            )

            if lotsman_documents_hierarcy_view_record.parent_id is not None:
                while True:
                    try:
                        item = Item.objects.get(lotsman_document_id=lotsman_documents_hierarcy_view_record.id, )
                        top_item = item
                        break
                    except Item.DoesNotExist:
                        if lotsman_documents_hierarcy_view_record.parent_id is not None:
                            lotsman_documents_hierarcy_view_record = Lotsman_documents_hierarcy_view.objects.get(id=lotsman_documents_hierarcy_view_record.parent_id)
                            if lotsman_documents_hierarcy_view_record.parent_id is None:
                                top_item.lotsman_document_id = lotsman_documents_hierarcy_view_record.id
                                if lotsman_documents_hierarcy_view_record._Version:
                                    top_item.version = lotsman_documents_hierarcy_view_record._Version.value_int,
                                if lotsman_documents_hierarcy_view_record._Type:
                                    top_item.lotsman_type_id = lotsman_documents_hierarcy_view_record._Type.value_int,
                                top_item.save()
                                break
                        else:
                            break
                    except Item.MultipleObjectsReturned:
                        item = Item.objects.filter(lotsman_document_id=lotsman_documents_hierarcy_view_record.id, )[0]
                        top_item = item
                        break

            parent_str = f'''parent_id ={lotsman_documents_hierarcy_view_record.id}'''
            props_str = 'props in (1, 3)'

            sql_str = f'''WITH RECURSIVE r AS (
                               SELECT *, 1 AS level
                               FROM kd_lotsman_documents_hierarcy_mview
                               WHERE {parent_str}
                                     and  {props_str}  

                               union all

                               SELECT kd_lotsman_documents_hierarcy_mview.*, r.level + 1 AS level
                               FROM kd_lotsman_documents_hierarcy_mview
                                   JOIN r
                               ON kd_lotsman_documents_hierarcy_mview.parent_id = r.id)

                           select * from r where {props_str} order by level'''

            mat_view_name = create_tmp_mat_view(sql_str=sql_str, indexes=['attr_name', 'parent_id'],check_exists=True)

            with connection.cursor() as cursor:
                cursor.execute(f'select count(*) from {mat_view_name} where props=1')
                cnt, = cursor.fetchone()

            # logger.logging(f'''SPC_CLM_NAME: {lotsman_documents_hierarcy_view_record.SPC_CLM_NAME.value_str}''', 'debug')
            # logger.logging(f'qty: {cnt}', 'debug')

            if cnt > 0:
                with managed_progress(
                        id=lotsman_documents_hierarcy_view_record.id,
                        qty=cnt,
                        user=self.user,
                        message=f'''Создание товарных позиций ({lotsman_documents_hierarcy_view_record.SPC_CLM_NAME.value_str} {cnt} шт.)''',
                        title='Выполнено',
                        props=TurnBitOn(0, 0)
                ) as progress:
                    with transaction.atomic():

                        # Tmp_Item_refsManager.create()
                        for lotsman_documents_hierarcy in Lotsman_documents_hierarcy_view.objects.raw(f'''select * from {mat_view_name}  where props=1 order by level'''):
                            if lotsman_documents_hierarcy.attr_name not in ['Материал']:

                                item, created1 = self.get_item(
                                    lotsman_documents_hierarcy=lotsman_documents_hierarcy,
                                    items_pairs=items_pairs,
                                )

                                if lotsman_documents_hierarcy.parent_id is not None:
                                    try:
                                        _lotsman_documents_hierarcy = Lotsman_documents_hierarcy_view.objects.get(id=lotsman_documents_hierarcy.parent_id)
                                    except Lotsman_documents_hierarcy_view.DoesNotExist as ex:
                                        raise ex
                                    except Lotsman_documents_hierarcy_view.MultipleObjectsReturned:
                                        _lotsman_documents_hierarcy = Lotsman_documents_hierarcy_view.objects.filter(id=lotsman_documents_hierarcy.parent_id).filter()[0]

                                    parent, created2 = self.get_item(
                                        lotsman_documents_hierarcy=_lotsman_documents_hierarcy,
                                        items_pairs=items_pairs,
                                    )

                                    item_refs, created2 = Item_refs.objects.get_or_create(parent=parent, child=item)

                                # FOR DEBUG
                                # if created == True or created1 == True or created2 == True:
                                #     pass
                                # END FOR DEBUG

                            else:
                                Lotsman_documents_hierarcy.objects.update_or_create(
                                    id=lotsman_documents_hierarcy.id,
                                    defaults=dict(
                                        props=lotsman_documents_hierarcy.props | Lotsman_documents_hierarcy.props.beenItemed
                                    ))

                            res = progress.step()
                            if res != 0:
                                raise ProgressDroped(progress_deleted)

                        progress.close()
                        with connection.cursor() as cursor:
                            cursor.execute(f'''select count(*) from {mat_view_name} where props=1 and attr_name=%s''', ['''Сборочная единица'''])
                            assmbl_progress_count, = cursor.fetchone()

                        with managed_progress(
                                id=f'''assmbl_{lotsman_documents_hierarcy_view_record.id}''',
                                qty=assmbl_progress_count,
                                user=self.user,
                                message=f'''Создание сборочных единиц. ({assmbl_progress_count}  шт.)''',
                                title='Выполнено',
                                props=TurnBitOn(0, 0)
                        ) as assmbl_progress:

                            # logger.logging(f'''Сборочные единицы SPC_CLM_NAME: {lotsman_documents_hierarcy_view_record.SPC_CLM_NAME.value_str}''', 'debug')
                            # logger.logging(f'qty: {assmbl_progress_count}', 'debug')

                            for lotsman_documents_hierarcy in Lotsman_documents_hierarcy_view.objects.raw(f'''select * from {mat_view_name} where props=1 and attr_name=%s order by level''', ['''Сборочная единица''']):

                                assmbl_progress.setContentsLabel(f'''<h3>Создание сборочной единицы. ({lotsman_documents_hierarcy.SPC_CLM_NAME.value_str if lotsman_documents_hierarcy.SPC_CLM_NAME else ''} : 
                                                                                                      {lotsman_documents_hierarcy.SPC_CLM_MARK.value_str if lotsman_documents_hierarcy.SPC_CLM_MARK else ''})</h3>''')
                                item, _ = self.get_item(
                                    lotsman_documents_hierarcy=lotsman_documents_hierarcy,
                                    items_pairs=items_pairs,
                                )

                                self.make_lines(
                                    parent=item,
                                    items_pairs=items_pairs,
                                    mat_view_name=mat_view_name,
                                    user_id=self.user,
                                    record=lotsman_documents_hierarcy_view_record,
                                )

                                Lotsman_documents_hierarcy.objects.update_or_create(
                                    id=lotsman_documents_hierarcy.id,
                                    defaults=dict(
                                        props=lotsman_documents_hierarcy.props | Lotsman_documents_hierarcy.props.beenItemed
                                    ))

                                res = assmbl_progress.step()
                                if res != 0:
                                    raise ProgressDroped(progress_deleted)

                        with connection.cursor() as cursor:
                            cursor.execute(f'''select count(*) from {mat_view_name} where props=1 and attr_name=%s''', ['''Чертеж'''])
                            assmbl_progress_count, = cursor.fetchone()

                        with managed_progress(
                                id=f'''assmbl_{lotsman_documents_hierarcy_view_record.id}''',
                                qty=assmbl_progress_count,
                                user=self.user,
                                message=f'''Привязка чертежей. ({assmbl_progress_count}  шт.)''',
                                title='Выполнено',
                                props=TurnBitOn(0, 0)
                        ) as assmbl_progress:

                            # logger.logging(f'''Чертежи SPC_CLM_NAME: {lotsman_documents_hierarcy_view_record.SPC_CLM_NAME.value_str}''', 'debug')
                            # logger.logging(f'qty: {assmbl_progress_count}', 'debug')

                            for lotsman_documents_hierarcy in Lotsman_documents_hierarcy_view.objects.raw(f'''select * from {mat_view_name} where props=1 and attr_name=%s order by level''', ['''Чертеж''']):

                                assmbl_progress.setContentsLabel(f'''<h3>Привязка чертежей. ({lotsman_documents_hierarcy.SPC_CLM_NAME.value_str if lotsman_documents_hierarcy.SPC_CLM_NAME else ''} :
                                                                                            {lotsman_documents_hierarcy.SPC_CLM_MARK.value_str if lotsman_documents_hierarcy.SPC_CLM_MARK else ''})</h3>''')
                                item, _ = self.get_item(
                                    lotsman_documents_hierarcy=lotsman_documents_hierarcy,
                                    items_pairs=items_pairs,
                                )

                                for item_ref in Item_refs.objects.filter(child=item):
                                    if item_ref.parent.lotsman_document.attr_type.code != 'Сборочная единица':
                                        self.documentManagerExt.link_image_to_lotsman_item(
                                            lotsman_document=lotsman_documents_hierarcy,
                                            item=item_ref.parent,
                                        )
                                        item_ref.delete()

                                Lotsman_documents_hierarcy.objects.update_or_create(
                                    id=lotsman_documents_hierarcy.id,
                                    defaults=dict(
                                        props=lotsman_documents_hierarcy.props | Lotsman_documents_hierarcy.props.beenItemed
                                    ))

                                res = assmbl_progress.step()
                                if res != 0:
                                    raise ProgressDroped(progress_deleted)

                        with managed_progress(
                                id=f'''assmbl_{lotsman_documents_hierarcy_view_record.id}''',
                                qty=assmbl_progress_count,
                                user=self.user,
                                message=f'''Перемещение чертежей. ({assmbl_progress_count}  шт.)''',
                                title='Выполнено',
                                props=TurnBitOn(0, 0)
                        ) as assmbl_progress:

                            for lotsman_documents_hierarcy in Lotsman_documents_hierarcy_view.objects.raw(f'''select * from {mat_view_name} where props=1 and attr_name=%s order by level''', ['''Чертеж''']):
                                item, _ = self.get_item(
                                    lotsman_documents_hierarcy=lotsman_documents_hierarcy,
                                    items_pairs=items_pairs,
                                )

                                if Item_refs.objects.filter(child=item).count() == 0 and Item_refs.objects.filter(parent=item).count() == 0:
                                    item.delete()

                                res = assmbl_progress.step()
                                if res != 0:
                                    raise ProgressDroped(progress_deleted)

            # FOR DEBUG
            with connection.cursor() as cursor:
                cursor.execute('''select count(*) from kd_lotsman_documents_hierarcy where props=1''')
                count, = cursor.fetchone()
            # END FOR DEBUG

            drop_mat_view(mat_view_name)
        except Exception as ex:
            drop_mat_view(mat_view_name)
            raise ex

    def make_lines(self, parent, items_pairs, mat_view_name, user_id, record):
        from kaf_pas.ckk.models.item import Item
        from kaf_pas.kd.models.lotsman_documents_hierarcy_view import Lotsman_documents_hierarcy_view
        from kaf_pas.ckk.models.item_line import Item_line
        from kaf_pas.ckk.models.item_line import Item_lineManager

        if not isinstance(parent, Item):
            raise Exception('item mut be Item instnce.')

        with connection.cursor() as cursor:
            cursor.execute(f'select count(*) from {mat_view_name} where parent_id=%s', [parent.lotsman_document.id])
            count, = cursor.fetchone()

        # logger.logging(f'parent.lotsman_document: {parent.lotsman_document}', 'debug')
        # logger.logging(f'qty: {count}', 'debug')

        with managed_progress(
                id=f'''lines_{parent.id}''',
                qty=count,
                user=user_id,
                message=f'''Создание строк детализации. ({parent.item_name}) ({count} строк.)''',
                title='Выполнено'
        ) as lines_progress:
            for lotsman_documents_hierarcy in Lotsman_documents_hierarcy_view.objects.raw(f'select * from {mat_view_name} where parent_id=%s order by level', [parent.lotsman_document.id]):
                item, _ = self.get_item(
                    lotsman_documents_hierarcy=lotsman_documents_hierarcy,
                    items_pairs=items_pairs,
                )

                if lotsman_documents_hierarcy.attr_name != 'Материал':

                    if lotsman_documents_hierarcy.section is None:
                        if lotsman_documents_hierarcy.attr_name in ['Чертеж', 'Спецификация']:
                            lotsman_documents_hierarcy.section = 'Документация'
                        elif lotsman_documents_hierarcy.attr_name in ['Сборочная единица']:
                            lotsman_documents_hierarcy.section = 'Сборочные единицы'
                        elif lotsman_documents_hierarcy.attr_name in ['Деталь']:
                            lotsman_documents_hierarcy.section = 'Детали'

                    if lotsman_documents_hierarcy.section is None:
                        lotsman_documents_hierarcy.section = lotsman_documents_hierarcy.attr_name

                    Документ_на_материал = None
                    Наименование_материала = None
                    Документ_на_сортамент = None
                    Наименование_сортамента = None

                    for lotsman_documents_hierarcy_view in Lotsman_documents_hierarcy_view.objects.filter(parent_id=lotsman_documents_hierarcy.id):
                        if lotsman_documents_hierarcy_view.attr_name in ['Материал']:
                            Документ_на_материал = lotsman_documents_hierarcy_view.Документ_на_материал
                            Наименование_материала = lotsman_documents_hierarcy_view.Наименование_материала
                            Документ_на_сортамент = lotsman_documents_hierarcy_view.Документ_на_сортамент
                            Наименование_сортамента = lotsman_documents_hierarcy_view.Наименование_сортамента
                            break

                    item_line, created = Item_line.objects.update_or_create(
                        parent=parent,
                        child=item,
                        defaults=dict(
                            SPC_CLM_FORMAT=lotsman_documents_hierarcy.SPC_CLM_FORMAT,
                            SPC_CLM_ZONE=lotsman_documents_hierarcy.SPC_CLM_ZONE,
                            SPC_CLM_POS=lotsman_documents_hierarcy.SPC_CLM_POS,
                            SPC_CLM_MARK=lotsman_documents_hierarcy.SPC_CLM_MARK,
                            SPC_CLM_NAME=lotsman_documents_hierarcy.SPC_CLM_NAME,
                            SPC_CLM_COUNT=lotsman_documents_hierarcy.SPC_CLM_COUNT,
                            SPC_CLM_NOTE=lotsman_documents_hierarcy.SPC_CLM_NOTE,
                            SPC_CLM_MASSA=lotsman_documents_hierarcy.SPC_CLM_MASSA,
                            SPC_CLM_MATERIAL=lotsman_documents_hierarcy.SPC_CLM_MATERIAL if lotsman_documents_hierarcy.SPC_CLM_MATERIAL else Наименование_материала,
                            SPC_CLM_USER=lotsman_documents_hierarcy.SPC_CLM_USER,
                            SPC_CLM_KOD=lotsman_documents_hierarcy.SPC_CLM_KOD,
                            SPC_CLM_FACTORY=lotsman_documents_hierarcy.SPC_CLM_FACTORY,
                            Документ_на_материал=Документ_на_материал,
                            Наименование_материала=Наименование_материала,
                            Документ_на_сортамент=Документ_на_сортамент,
                            Наименование_сортамента=Наименование_сортамента,
                            section=lotsman_documents_hierarcy.section,
                            section_num=Item_lineManager.section_num(lotsman_documents_hierarcy.section),
                            subsection=lotsman_documents_hierarcy.subsection,
                        )
                    )

                lines_progress.step()

    def get_item(self, lotsman_documents_hierarcy, items_pairs):
        from kaf_pas.ckk.models.item import Item
        from kaf_pas.kd.models.lotsman_documents_hierarcy_refs import Lotsman_documents_hierarcy_refs

        items = [item[1] for item in items_pairs.stack if item[0] == lotsman_documents_hierarcy.id]
        if len(items) == 0:
            STMP_1 = lotsman_documents_hierarcy.SPC_CLM_NAME
            STMP_2 = lotsman_documents_hierarcy.SPC_CLM_MARK

            item, created = Item.objects.get_or_create(
                lotsman_document_id=lotsman_documents_hierarcy.id,
                version=lotsman_documents_hierarcy._Version.value_int if lotsman_documents_hierarcy._Version else None,
                lotsman_type_id=lotsman_documents_hierarcy._Type.value_int if lotsman_documents_hierarcy._Type else None,
                defaults=dict(
                    STMP_1=STMP_1,
                    STMP_2=STMP_2,
                    props=Item.props.relevant | Item.props.from_lotsman,
                )
            )

            if lotsman_documents_hierarcy.attr_name in ['Деталь']:
                for lotsman_documents_hierarcy_chert in Lotsman_documents_hierarcy_refs.objects.filter(
                        parent_id=lotsman_documents_hierarcy.id,
                        child__attr_type__code='Чертеж'):
                    self.documentManagerExt.link_image_to_lotsman_item(
                        lotsman_document=lotsman_documents_hierarcy_chert.child,
                        item=item,
                    )
            else:
                self.documentManagerExt.link_image_to_lotsman_item(
                    lotsman_document=lotsman_documents_hierarcy,
                    item=item,
                )

            items_pairs.push((lotsman_documents_hierarcy.id, item))

            # if logger and created:
            #     logger.logging(f'\nAdded parent: {item}', 'debug')

            return item, created
        elif len(items) == 1:
            return items[0], False
        else:
            raise Exception('Неоднозначный выбор.')

    def make_mview(self):
        from kaf_pas.system.models.contants import Contants
        from django.db import connection

        index_sql = []
        fields_sql = []
        sql_array = []

        parent_system_const, _ = Contants.objects.update_or_create(
            code='lotsman_attibutes',
            defaults=dict(name='Атрибуты товарных позиций импортированных из Лоцмана')
        )

        attr_map = {
            'Зона': 'SPC_CLM_ZONE',
            'Код': 'SPC_CLM_KOD',
            'Масса': 'SPC_CLM_MASSA',
            'Материал': 'SPC_CLM_MATERIAL',
            'Наименование': 'SPC_CLM_NAME',
            'Обозначение': 'SPC_CLM_MARK',
            'Позиция': 'SPC_CLM_POS',
            'Пользовательская': 'SPC_CLM_USER',
            'Предприятие - изготовитель': 'SPC_CLM_FACTORY',
            'Примечание': 'SPC_CLM_NOTE',
            'Формат': 'SPC_CLM_FORMAT',
        }

        for name, code in attr_map.items():
            Contants.objects.update_or_create(
                code=code,
                defaults=dict(
                    name=name,
                    parent=parent_system_const
                )
            )

        m_view_name = 'kd_lotsman_documents_hierarcy_mview'
        m_view_recurs_name = 'kd_lotsman_documents_hierarcy_recurs_view'

        sql_array.append(f'DROP VIEW IF EXISTS {m_view_recurs_name} CASCADE')
        sql_array.append(f'DROP MATERIALIZED VIEW IF EXISTS {m_view_name} CASCADE')
        sql_array.append(f'''CREATE MATERIALIZED VIEW {m_view_name} AS SELECT lts.id,
                                                                                      lts.deleted_at,
                                                                                      lts.editing,
                                                                                      lts.deliting,
                                                                                      lts.lastmodified,                                                                                
                                                                                      ltsr.parent_id,
                                                                                      lts.props,
                                                                                      lts.attr_type_id,
                                                                                      lts.document_id,
                                                                                      CASE
                                                                                           WHEN (select count(1) as count
                                                                                                 from kd_lotsman_documents_hierarcy_refs hr                                                            	
                                                                                                 where hr.parent_id = lts.id) > 0 THEN true
                                                                                           ELSE false
                                                                                      END AS "isFolder",                                                                  
                                                                                      ltsr.section,
                                                                                      ltsr.subsection,
                                                                                      att.code attr_code,
                                                                                      att.name attr_name
                                                                                      $COMMA
                                                                                      $FIELDS
                                                                               FROM kd_lotsman_documents_hierarcy lts
                                                                                       join kd_lotsman_documents_hierarcy_refs ltsr on ltsr.child_id = lts.id
                                                                                       join ckk_attr_type att on att.id = lts.attr_type_id WITH DATA;
                                                                                       --join ckk_attr_type att on att.id = lts.attr_type_id ;
                                                                               $INDEXES''')

        for field in ['id', 'deleted_at', 'editing', 'deliting', 'lastmodified', 'parent_id', 'props', 'attr_type_id', 'document_id', 'isFolder', 'section', 'subsection', 'attr_code', 'attr_name']:
            index_sql.append(f'''CREATE INDEX "ldh_attr_{field}_idx" ON {m_view_name} USING btree ("{field}")''')

        for field in Contants.objects.filter(parent__code='lotsman_attibutes'):
            fields_sql.append(f'''( SELECT kat.id
                                                  FROM kd_document_attributes kat
                                                    JOIN kd_lotsman_document_attr_cross dc ON kat.id = dc.attribute_id
                                                    JOIN ckk_attr_type att ON att.id = kat.attr_type_id
                                                 WHERE dc.document_id = ltsr.child_id and (dc.parent_document_id = ltsr.parent_id or ltsr.parent_id is null) AND att.code::text = '{field.code}'::text limit 1) AS "{field.code}_id"''')
            index_sql.append(f'''CREATE INDEX "ldh_attr_{field.code}_idx" ON {m_view_name} USING btree ("{field.code}_id")''')

        if len(fields_sql) > 0:
            sql_str = ';\n'.join(sql_array).replace('$FIELDS', ',\n'.join(fields_sql)).replace('$INDEXES', ';\n'.join(index_sql))
            sql_str = sql_str.replace('$COMMA', ',')
        else:
            sql_str = ';\n'.join(sql_array).replace('$FIELDS', '')
            sql_str = sql_str.replace('$COMMA', '')

        with connection.cursor() as cursor:
            # self.logger.logging(f'\n{sql_str}')
            cursor.execute(sql_str)
            # self.logger.logging(f'{m_view_name} recreated')

            sql_array = []
            sql_array.append(
                f'''CREATE VIEW {m_view_recurs_name} AS
                                                        select *
                                                        from (WITH RECURSIVE r AS (
                                                            SELECT *, 1 AS level
                                                            FROM {m_view_name}
                                                            WHERE parent_id IS NULL                                                        
                                                            union all
                                                            SELECT {m_view_name}.*, r.level + 1 AS level
                                                            FROM {m_view_name}
                                                                     JOIN r ON {m_view_name}.parent_id = r.id)
                                                              select *
                                                              from r
                                                              order by level) as a'''
            )
            sql_str = ';\n'.join(sql_array)
            # self.logger.logging(f'\n{sql_str}')
            cursor.execute(sql_str)
            # self.logger.logging(f'{m_view_recurs_name} recreated')
