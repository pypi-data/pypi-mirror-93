import logging

from django.db.models import TextField, CharField

from isc_common.auth.models.user import User
from isc_common.fields.code_field import CodeField
from isc_common.fields.description_field import DescriptionField
from isc_common.fields.name_field import NameField
from isc_common.fields.related import ForeignKeyProtect
from isc_common.managers.common_managet_with_lookup_fields import CommonManagetWithLookUpFieldsManager, CommonManagetWithLookUpFieldsQuerySet
from isc_common.models.audit import AuditModel
from kaf_pas.ckk.models.locations import Locations
from kaf_pas.input.models.user_positions import User_positions

logger = logging.getLogger(__name__)


class User_add_infoQuerySet(CommonManagetWithLookUpFieldsQuerySet):
    def filter(self, *args, **kwargs):
        return super().filter(*args, **kwargs)


class User_add_infoManager(CommonManagetWithLookUpFieldsManager):

    @classmethod
    def getRecord(cls, record):
        res = {
            'id': record.id,
            'ip_address': record.ip_address,
            'comp_name': record.comp_name,
            'user_agent': record.user_agent,
            'color': record.color,
            'description': record.description,
            'phones': record.phones,
            'location_id': record.location.id,
            'location__code': record.location.code,
            'location__name': record.location.name,
            'location__full_name': record.location.full_name,
            'position_id': record.position.id if record.position else None,
            'position__code': record.position.code if record.position else None,
            'position__name': record.position.name if record.position else None,
            'editing': record.editing,
            'deliting': record.deliting,
        }
        return res

    def get_queryset(self):
        return User_add_infoQuerySet(self.model, using=self._db)


class User_add_info(AuditModel):
    description = TextField(blank=True, null=True)
    comp_name = NameField()
    ip_address = CharField(max_length=20, null=True, blank=True)
    user_agent = TextField(null=True, blank=True)
    user = ForeignKeyProtect(User)
    location = ForeignKeyProtect(Locations)
    position = ForeignKeyProtect(User_positions, null=True, blank=True)
    color = CodeField()
    phones = DescriptionField()

    objects = User_add_infoManager()

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = 'Дополнительная пользовательская информация'
