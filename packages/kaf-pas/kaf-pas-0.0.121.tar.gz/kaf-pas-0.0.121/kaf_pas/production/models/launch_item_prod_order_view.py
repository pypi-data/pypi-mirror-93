import logging

from django.contrib.postgres.fields import ArrayField
from django.db.models import PositiveIntegerField, BooleanField, DecimalField, BigIntegerField

from isc_common.common import blinkString
from isc_common.fields.name_field import NameField
from isc_common.fields.related import ForeignKeyProtect, ForeignKeyCascade, ForeignKeySetNull
from isc_common.http.DSRequest import DSRequest
from isc_common.models.audit import AuditModel, AuditManager, AuditQuerySet
from isc_common.models.standard_colors import Standard_colors
from isc_common.number import DelProps, DecimalToStr
from kaf_pas.ckk.models.ed_izm import Ed_izm
from kaf_pas.ckk.models.item import Item_add, Item
from kaf_pas.ckk.models.item_line import Item_line, Item_lineManager
from kaf_pas.kd.models.document_attributes import Document_attributes

logger = logging.getLogger(__name__)


class Launch_item_order_viewQuerySet(AuditQuerySet):
    def get_range_rows2(self, request, function=None):
        request = DSRequest(request=request)
        # data = request.get_data()
        # delAttr(data, 'launch_id')
        # request.set_data(data)

        self.alive_only = request.alive_only
        self.enabledAll = request.enabledAll
        res = self.get_range_rows(
            start=request.startRow,
            end=request.endRow,
            function=function,
            json=request.json,
            criteria=request.get_criteria(),
            user=request.user
        )
        return res

    def get_range_rows(self, start=None, end=None, function=None, json=None, distinct_field_names=None, user=None, *args, **kwargs):
        from kaf_pas.production.models.launches import Launches
        from isc_common.common.functions import ExecuteStoredProcRows
        from kaf_pas.ckk.models.locations_users import Locations_users

        data = json.get('data')

        parent_id = data.get('parent_id')
        launch = Launches.objects.get(id=data.get('launch_id'))

        location_ids = list(set(map(lambda x: x.location.id, Locations_users.objects.filter(user=user))))
        if launch.parent is None:
            rows = ExecuteStoredProcRows(storedProcName='production_launch_item_prod_order', parametrs=[parent_id, launch.id, location_ids])
        else:
            rows = ExecuteStoredProcRows(storedProcName='production_launch_item_prod_order_per_launch', parametrs=[parent_id, launch.id, location_ids])

        res = []
        for row in rows:
            editing, deliting, section, section_num, subsection, SPC_CLM_MARK_id, SPC_CLM_NAME_id, deleted_at, child_id, parent_id, item_line_id, edizm_id, item_props, enabled, relevant, qty_per_one, where_from, color_id, _, qty_exists, _, _, _, _ = row
            color = Standard_colors.objects.get(id=color_id) if color_id is not None else None
            edizm = Ed_izm.objects.get(id=edizm_id) if edizm_id is not None else None
            SPC_CLM_NAME = Document_attributes.objects.get(id=SPC_CLM_NAME_id) if SPC_CLM_NAME_id is not None else None
            SPC_CLM_MARK = Document_attributes.objects.get(id=SPC_CLM_MARK_id) if SPC_CLM_MARK_id is not None else None

            res.append(dict(
                child_id=child_id,
                color__color=color.color if color and color else None,
                color__name=color.name if color and color else None,
                color_id=color_id,
                deleted_at=deleted_at,
                deliting=deliting,
                editing=editing,
                edizm__name=edizm.name if edizm else None,
                edizm_id=edizm_id,
                enabled=enabled,
                id=child_id,
                item_line_id=item_line_id,
                item_props=item_props,
                parent_id=parent_id,
                qty_exists=DecimalToStr(qty_exists),
                qty_per_one=DecimalToStr(qty_per_one),
                relevant=relevant,
                section=section,
                section_num=section_num,
                SPC_CLM_MARK__value_str=SPC_CLM_MARK.value_str if SPC_CLM_MARK else None,
                SPC_CLM_MARK_id=SPC_CLM_MARK_id,
                SPC_CLM_NAME__value_str=SPC_CLM_NAME.value_str if SPC_CLM_NAME else None,
                SPC_CLM_NAME_id=SPC_CLM_NAME_id,
                subsection=subsection,
                where_from=where_from,
            ))
        return res


class Launch_item_order_viewManager(AuditManager):

    @classmethod
    def get_buffer_oddment_value(cls, value):
        if value is None:
            return None
        return blinkString(text=DecimalToStr(value), blink=True if value < 0 else False, bold=True, color='green' if value > 0 else 'red')

    @classmethod
    def getRecord(cls, record):
        res = {
            'child_id': record.child.id,
            'color__color': record.color.color if record.color and record.color else None,
            'color__name': record.color.name if record.color and record.color else None,
            'color_id': record.color.id if record.color and record.color else None,
            'deliting': record.deliting,
            'editing': record.editing,
            'edizm__name': record.edizm.name if record.edizm else None,
            'edizm_id': record.edizm.id if record.edizm else None,
            'enabled': record.enabled,
            'id': record.id,
            'item_props': record.item_props,
            'lastmodified': record.lastmodified,
            'parent_id': record.parent.id,
            'qty_exists': Launch_item_order_viewManager.get_buffer_oddment_value(record.qty_exists),
            'qty_per_one': DecimalToStr(record.qty_per_one) if record.section != 'Документация' else None,
            'relevant': record.relevant,
            'section': record.section,
            'section_num': Item_lineManager.section_num(record.section),
            'SPC_CLM_MARK__value_str': record.SPC_CLM_MARK.value_str if record.SPC_CLM_MARK else None,
            'SPC_CLM_MARK_id': record.SPC_CLM_MARK.id if record.SPC_CLM_MARK else None,
            'SPC_CLM_NAME__value_str': record.SPC_CLM_NAME.value_str if record.SPC_CLM_NAME else None,
            'SPC_CLM_NAME_id': record.SPC_CLM_NAME.id if record.SPC_CLM_NAME else None,
            'subsection': record.subsection,
            'where_from': record.where_from,
        }
        return DelProps(res)

    def get_queryset(self):
        return Launch_item_order_viewQuerySet(self.model, using=self._db)


class Launch_item_order_view(AuditModel):
    parent = ForeignKeyProtect(Item, verbose_name='Товарная позиция', related_name='item_parent_p')
    child = ForeignKeyCascade(Item, verbose_name='Товарная позиция', related_name='item_child_p')

    SPC_CLM_MARK = ForeignKeyProtect(Document_attributes, verbose_name='Обозначение', related_name='SPC_CLM_MARK_p', null=True, blank=True)
    SPC_CLM_NAME = ForeignKeyProtect(Document_attributes, verbose_name='Наименование', related_name='SPC_CLM_NAME_p', null=True, blank=True)

    item = ForeignKeyProtect(Item, related_name='Item_p')
    edizm = ForeignKeyProtect(Ed_izm, verbose_name='Единица измерения', related_name='EdIzm_p', null=True, blank=True)
    section = NameField()
    section_num = PositiveIntegerField(default=0)
    subsection = NameField()
    item_line = ForeignKeySetNull(Item_line, null=True, blank=True)
    color = ForeignKeyProtect(Standard_colors, null=True, blank=True, related_name='Launch_item_order_view_color')
    colorb = ForeignKeyProtect(Standard_colors, null=True, blank=True, related_name='Launch_item_order_view_colorb')
    launch_ids = ArrayField(BigIntegerField(), default=list)

    # qty_doc = DecimalField(decimal_places=4, max_digits=19)
    qty_per_one = DecimalField(decimal_places=4, max_digits=19)
    qty_exists = DecimalField(decimal_places=4, max_digits=19, null=True, blank=True)
    # qty_odd = DecimalField(decimal_places=4, max_digits=19, null=True, blank=True)

    where_from = NameField()
    item_props = Item_add.get_prop_field()
    relevant = NameField()
    enabled = BooleanField()

    objects = Launch_item_order_viewManager()

    def __str__(self):
        return f'child: [{self.child}], qty_exists: {self.qty_exists}'

    class Meta:
        verbose_name = 'Строка состава изделия в производственной спецификации'
        db_table = 'production_launch_item_prod_order_view'
        managed = False
