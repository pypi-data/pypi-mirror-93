import logging

from django.db.models import Sum

from isc_common.common import sht
from isc_common.number import ToDecimal, ToStr, DecimalToStr
from kaf_pas.accounting.models.buffer_ext import Buffer_ext

logger = logging.getLogger(__name__)


class Production_order_tmp_ext:
    buffer_ext = Buffer_ext()

    def update_absorption(self, id, value_made, user):
        from kaf_pas.planing.models.production_order_tmp import Production_order_tmpManager
        from kaf_pas.planing.models.production_order_tmp import Production_order_tmp

        for production_order_tmp in Production_order_tmp.objects.filter(id=id, props=Production_order_tmp.props.absorption):
            if value_made == 0:
                production_order_tmp.value_made = value_made
                production_order_tmp.save()
                continue

            complect_qty = self.buffer_ext.get_max_complect(
                item_id=production_order_tmp.item_id,
                launch_id=production_order_tmp.launch.id,
                location_id=production_order_tmp.location.id,
                resource_id=production_order_tmp.resource.id,
                color_id=production_order_tmp.color.id if production_order_tmp.color is not None else None)

            if value_made > complect_qty:
                raise Exception(f'Превышение остатка, возможная величина: {complect_qty}')

            for complect in self.buffer_ext.get_launches_complects(
                    item_id=production_order_tmp.item_id,
                    total_qty=value_made,
                    launch_id=production_order_tmp.launch.id,
                    location_id=production_order_tmp.location.id,
                    resource_id=production_order_tmp.resource.id,
                    color_id=production_order_tmp.color.id if production_order_tmp.color is not None else None):
                for item in complect.get('items'):
                    for updating_production_order_tmp in Production_order_tmp.objects.filter(
                            parent_id=production_order_tmp.id_f,
                            launch_id=production_order_tmp.launch.id,
                            item_id=item.item_id,
                            props=Production_order_tmp.props.qty_not_editing
                    ):
                        updating_production_order_tmp.value_made = item.value_used
                        updating_production_order_tmp.save()

                        Production_order_tmpManager.refreshRows(ids=updating_production_order_tmp.id, user=user)

    def set_Count(self, data, user):
        from kaf_pas.ckk.models.ed_izm import Ed_izm
        from kaf_pas.planing.models.production_order_tmp import Production_order_tmp
        from kaf_pas.planing.models.production_order_tmp import Production_order_tmpManager

        process = data.get('process')
        value = None
        if data.get('value') is not None:
            value = ToDecimal(data.get('value'))
        value_absorption = value
        count = 0

        edizm = Ed_izm.objects.get(code=sht)
        if process is not None:
            ids = []
            for production_order_tmp in Production_order_tmp.objects.filter(process=process).exclude(enabled=False):
                if value is not None:
                    value_made = value * production_order_tmp.parent_mul
                else:
                    value_made = production_order_tmp.value_start
                    value_absorption = production_order_tmp.value_start

                if production_order_tmp.launch_incom is None:
                    if value_made > production_order_tmp.value_odd:
                        raise Exception(f'По {production_order_tmp.item.item_name} Превышение остатка, возможная величина: {ToStr(production_order_tmp.value_odd)}')
                else:
                    launches_odd = production_order_tmp.launches_odd

                    odd = list(filter(lambda x: x.get('launch_id') == production_order_tmp.launch_incom.id, launches_odd))
                    if len(odd) > 0:
                        odd = odd[0]
                        process = production_order_tmp.process
                        value_made__sum = Production_order_tmp.objects.filter(process=process, launch_incom=production_order_tmp.launch_incom, item_id=production_order_tmp.item_id).exclude(id=production_order_tmp.id).aggregate(Sum('value_made'))
                        value_made__sum = value_made__sum.get('value_made__sum')

                        if ToDecimal(odd.get('value_odd')) < ToDecimal(value_made) + ToDecimal(value_made__sum):
                            raise Exception(f'Превищение суммы по запуску ({ToStr(value_made)}), возможная величина: {ToStr(ToDecimal(odd.get("value_odd")) - ToDecimal(value_made__sum))}')

                if production_order_tmp.props.absorption.is_set and not production_order_tmp.props.qty_not_editing.is_set:
                    if value_absorption > production_order_tmp.value_made_old:
                        value_absorption -= production_order_tmp.value_made_old
                        self.update_absorption(id=production_order_tmp.id, value_made=production_order_tmp.value_made_old, user=user)
                    else:
                        self.update_absorption(id=production_order_tmp.id, value_made=value_absorption, user=user)
                        production_order_tmp.value_made = value_absorption
                        value_absorption = 0

                    production_order_tmp.edizm = edizm
                    production_order_tmp.save()
                    ids.append(production_order_tmp.id)

                    ids.append(production_order_tmp.id)
                elif not production_order_tmp.props.qty_not_editing.is_set:
                    production_order_tmp.value_made = value_made
                    production_order_tmp.edizm = edizm
                    production_order_tmp.save()

                    ids.append(production_order_tmp.id)
                    # logger.debug(f'\nprocess:{process}')
                    # logger.debug(f'\ncount:{count}')
                    count += 1

            Production_order_tmpManager.refreshRows(ids=ids, user=user)
        return dict(count=1)

    def get_Count(self, data):
        from kaf_pas.planing.models.production_order_tmp import Production_order_tmp
        process = data.get('process')
        count = 0
        if process is not None:
            count = Production_order_tmp.objects.filter(process=process, value_made__isnull=False).exclude(value_made=0).count()
            logger.debug(f'\nprocess:{process}')
            logger.debug(f'\ncount:{count}')
        return dict(count=count)

    def get_Check(self, data, user):
        from kaf_pas.planing.models.production_ext import Production_ext

        process = data.get('process')
        errors = []
        if process is not None:
            production_ext = Production_ext()
            errors = production_ext.check_selected_order_4_finish(data=data, user=user)
            logger.debug(f'\nprocess:{process}')
        return dict(errors=errors)
