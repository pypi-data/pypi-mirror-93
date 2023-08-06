import logging

from django.core.management import BaseCommand

from isc_common.common.functions import delete_dbl_spaces
from kaf_pas.kd.models.pathes import Pathes
from django.db import transaction

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Тестирование"

    def handle(self, *args, **options):
        kwargs = dict(
            path = 'Y:\\Архив\\Гражданские кузова_17-11-2020\\К4310\\ПапкаК4310..xml',
            parent = None,
            with_out_last = True
        )
        with transaction.atomic():
            Pathes.objects.create_ex_with_check(**kwargs)
