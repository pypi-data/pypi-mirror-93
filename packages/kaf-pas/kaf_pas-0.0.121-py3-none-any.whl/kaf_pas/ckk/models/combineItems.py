import logging

from django.db import transaction

from isc_common import delAttr, setAttr
from isc_common.http.DSRequest import DSRequest
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.number import model_2_dict
from kaf_pas.ckk.models.item import Item
from kaf_pas.ckk.models.item_image_refs import Item_image_refs
from kaf_pas.ckk.models.item_refs import Item_refs
from kaf_pas.sales.models.precent_items import Precent_items

logger = logging.getLogger(__name__)


class CombineItems(DSRequest):
    @classmethod
    def combine(cls, recordTarget, recordsSource):

        with transaction.atomic():
            for recordSource in recordsSource:
                if recordSource.get('id') != recordTarget.get('id'):
                    for item_refs in Item_refs.objects.filter(child_id=recordSource.get('id')):
                        cnt = Item_refs.objects.filter(child_id=recordTarget.get('id'), parent=item_refs.parent,props=item_refs.props).count()
                        if cnt == 0:
                            item_refs.child_id = recordTarget.get('id')
                            item_refs.save()

                    for item_image_refs in Item_image_refs.objects.filter(item_id=recordSource.get('id')):
                        dict = model_2_dict(item_image_refs)

                        delAttr(dict, 'id')
                        delAttr(dict, 'deleted_at')
                        setAttr(dict, 'item_id', recordTarget.get('id'))

                        res, created = Item_image_refs.objects.get_or_create(**dict)
                        if not created:
                            res.soft_restore()
                        item_image_refs.soft_delete()

                    for precent_item in Precent_items.objects.filter(item_id=recordSource.get('id')):
                        precent_item.item_id = recordTarget.get('id')
                        precent_item.save()

                    res = Item.objects.filter(id=recordSource.get('id')).soft_delete()
                    logger.debug(f'deleted Item ({res})')

    def __init__(self, request):
        DSRequest.__init__(self, request)
        data = self.get_data()

        recordTarget = data.get('recordTarget')
        if not isinstance(recordTarget, dict):
            raise Exception('recordTarget must be a dict')

        recordsSource = data.get('recordsSource')
        if not isinstance(recordsSource, list):
            raise Exception('recordsSource must be a list')

        # with transaction.atomic():
        CombineItems.combine(recordsSource=recordsSource, recordTarget=recordTarget)

        self.response = dict(status=RPCResponseConstant.statusSuccess)
