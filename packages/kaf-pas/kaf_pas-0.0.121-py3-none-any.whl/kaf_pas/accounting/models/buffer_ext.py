import logging

from django.db.models import Sum

from isc_common import Wrapper, setAttr, Stack
from isc_common.datetime import DateToStr
from isc_common.number import ToStr, model_2_dict, ToDecimal
from kaf_pas.ckk.models.item import Item
from kaf_pas.planing.models.production_order_values_ext import Production_order_values_ext
from kaf_pas.production.models.launches import Launches

logger = logging.getLogger(__name__)


class BufferWrapper(Wrapper):
    color = None
    color_id = None
    demand = None
    demand_id = None
    edizm = None
    edizm_id = None
    item = None
    item_id = None
    last_operation = None
    last_operation_id = None
    last_tech_operation_id = None
    launch = None
    launch_id = None
    location = None
    location_fin = None
    location_id = None
    resource = None
    resource_fin = None
    resource_id = None
    value = None
    value_used = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.color_id is not None:
            from isc_common.models.standard_colors import Standard_colors
            self.color = Standard_colors.objects.get(id - self.color_id)

        if self.demand_id is not None:
            from kaf_pas.sales.models.demand import Demand
            self.demand = Demand.objects.get(id=self.demand_id)

        if self.edizm_id is not None:
            from kaf_pas.ckk.models.ed_izm import Ed_izm
            self.edizm = Ed_izm.objects.get(id=self.edizm_id)

        if self.item_id is not None:
            from kaf_pas.ckk.models.item import Item
            self.item = Item.objects.get(id=self.item_id)

        if self.last_operation_id is not None:
            from kaf_pas.production.models.operations import Operations
            self.last_operation = Operations.objects.get(id=self.last_operation_id)

        if self.last_tech_operation_id is not None:
            from kaf_pas.planing.models.operations import Operations
            self.last_tech_operation = Operations.objects.get(id=self.last_tech_operation_id)

        if self.launch_id is not None:
            self.launch = Launches.objects.get(id=self.launch_id)

        if self.location_id is not None:
            from kaf_pas.ckk.models.locations import Locations
            self.location = Locations.objects.get(id=self.location_id)

        if self.resource_id is not None:
            from kaf_pas.production.models.resource import Resource
            self.resource = Resource.objects.get(id=self.resource_id)


class Buffer_ext:
    production_order_values_ext = Production_order_values_ext()

    def get_max_complect(self, item_id, launch_id, location_id, resource_id=None, color_id=None):
        from kaf_pas.accounting.models.buffers import Buffers
        from kaf_pas.ckk.models.item import Item
        from kaf_pas.ckk.models.locations import Locations
        from kaf_pas.production.models.launch_item_line_view import Launch_item_line_view
        from kaf_pas.production.models.launch_item_view import Launch_item_view
        from kaf_pas.production.models.launches import Launches

        item = Item.objects.get(id=item_id)
        # logger.debug(f'item: {item.item_name}')

        location = Locations.objects.get(id=location_id)
        # logger.debug(f'location: {location.full_name}')

        launch = Launches.objects.get(id=launch_id)
        _launch = launch
        if launch.parent is None:
            _launch = launch.child_launches[0]
        # logger.debug(f'launch: {launch.code}')
        res = []

        childs_line_query = Launch_item_line_view.objects.filter(parent=item, launch=_launch).exclude(section='Документация')
        childs_line = set(map(lambda x: x.child.id, childs_line_query))
        childs_item = set(map(lambda x: x.id, Launch_item_view.objects.filter(parent_id=item.id, launch=launch).exclude(section='Документация')))
        intersect = childs_item.difference(childs_line)
        if len(intersect) > 0:
            raise Exception(f'Для {item.item_name} детализация не совпадает с составом.')

        for launch_item_line in childs_line_query:
            buffer = Buffers.objects.filter(item=launch_item_line.child, launch=launch)

            if resource_id is not None:
                buffer = buffer.filter(resource_id=resource_id)
            else:
                buffer = buffer.filter(location=location)

            if color_id is not None:
                buffer = buffer.filter(color_id=color_id)

            value__sum = buffer.aggregate(Sum('value'))
            value__sum = value__sum.get('value__sum')
            if value__sum is not None:
                res.append(value__sum // launch_item_line.qty_per_one)

        if isinstance(res, list) and len(res) > 0:
            res = min(res)
        else:
            res = 0
        return res

    def get_complect_total_qty(self, item_id, launch_id, location_id, resource_id=None, color_id=None):

        res = 0
        launch = Launches.objects.get(id=launch_id)
        item = Item.objects.get(id=item_id)
        # logger.debug(f'launch: {launch.code}')

        if launch.parent is not None:
            launches = [launch]
        else:
            launches = self.production_order_values_ext.get_launches(parent_launch=launch, item=item)
            launches.append(launch)

        for _launch in launches:
            res += self.get_max_complect(item_id=item_id, launch_id=_launch.id, location_id=location_id, resource_id=resource_id, color_id=color_id)
        return res

    def get_launches_complects(self, total_qty, item_id, launch_id, location_id, resource_id=None, color_id=None, with_out_view=False):
        from kaf_pas.production.models.launch_item_line_view import Launch_item_line_view
        from kaf_pas.accounting.models.buffers import Buffers

        launch = Launches.objects.get(id=launch_id)
        item = Item.objects.get(id=item_id)
        # logger.debug(f'launch: {launch.code}')

        if launch.parent is not None:
            launches = [launch]
        else:
            launches = self.production_order_values_ext.get_launches(parent_launch=launch, item=item)
            launches.append(launch)

        stack_res = Stack()
        for _launch in launches:
            _launch_rel = _launch
            stack_launches = Stack()

            if total_qty == 0:
                break

            if _launch.parent is None:
                _launch = _launch.child_launches[0]

            complect_qty = self.get_max_complect(item_id=item_id, launch_id=_launch_rel.id, location_id=location_id, resource_id=resource_id, color_id=color_id)
            _complect_qty = complect_qty

            if complect_qty > 0:
                if complect_qty < total_qty:
                    total_qty -= complect_qty
                else:
                    complect_qty = total_qty
                    total_qty = 0

                childs_line_query = Launch_item_line_view.objects.filter(parent_id=item_id, launch=_launch).exclude(section='Документация')
                for launch_item_line in childs_line_query:

                    buffer_query = Buffers.objects.filter(item=launch_item_line.child, launch=_launch_rel)

                    if resource_id is not None:
                        buffer_query = buffer_query.filter(resource_id=resource_id)
                    else:
                        buffer_query = buffer_query.filter(location_id=location_id)

                    if color_id is not None:
                        buffer_query = buffer_query.filter(color_id=color_id)

                    value__sum = buffer_query.aggregate(Sum('value'))
                    value__sum = ToDecimal(value__sum.get('value__sum'))

                    value_used = launch_item_line.qty_per_one * complect_qty

                    if value_used > value__sum:
                        raise Exception(f'Превышение наличия для {launch_item_line.child.item_name}, затребовано {ToStr(value_used)}, в наличии {ToStr(value__sum)}, запуск {_launch.code} от {DateToStr(_launch.date)}')

                    for buffer in buffer_query:
                        if value_used > buffer.value:
                            value = buffer.value
                            value_used -= value
                        elif value_used == 0:
                            value = 0
                        else:
                            value = value_used
                            value_used = 0

                        if resource_id is not None and resource_id != buffer.resource.id:
                            raise Exception('Двойной ресурс')

                        resource_id = buffer.resource.id
                        buffer_dict = model_2_dict(buffer)
                        setAttr(buffer_dict, 'value_used', value)
                        setAttr(buffer_dict, 'value_used_old', value)
                        setAttr(buffer_dict, 'value_sum', launch_item_line.qty_doc)
                        setAttr(buffer_dict, 'value1_sum', launch_item_line.qty_per_one)
                        setAttr(buffer_dict, 'value_start', buffer.value)
                        stack_launches.push(BufferWrapper(**buffer_dict))

            stack_res.push(dict(
                launch_id=_launch_rel.id,
                location_id=location_id,
                resource_id=resource_id,
                demand_id=_launch_rel.demand_id,
                complect_qty=_complect_qty,
                items=stack_launches))

        if with_out_view is True and total_qty > 0:
            raise Exception(f'Нехватка для {total_qty} комплектов.')

        return stack_res
