import logging

from bitfield import BitField
from django.db import transaction
from django.db.models import UniqueConstraint, Q

from isc_common import setAttr
from isc_common.auth.models.user import User
from isc_common.fields.related import ForeignKeyCascade
from isc_common.http.DSRequest import DSRequest
from isc_common.models.audit import AuditManager, AuditQuerySet
from isc_common.models.base_ref import Hierarcy
from isc_common.number import DelProps
from kaf_pas.ckk.models.locations import Locations

logger = logging.getLogger(__name__)


class Locations_usersQuerySet(AuditQuerySet):
    pass


class Locations_usersManager(AuditManager):

    def createFromRequest(self, request, removed=None):
        request = DSRequest(request=request)
        data = request.get_data()
        user_ids = data.get('user_ids', None)
        context_ids = data.get('context_ids', None)
        parent_ids = data.get('parent_ids', None)

        with transaction.atomic():
            if user_ids and context_ids:
                if not isinstance(user_ids, list):
                    user_ids = [user_ids]

                if not isinstance(context_ids, list):
                    context_ids = [context_ids]

                if parent_ids:
                    for parent_id in parent_ids:
                        for user_id in user_ids:
                            for context_id in context_ids:
                                super().get_or_create(parent_id=parent_id, user_id=user_id, location_id=context_id)
                else:
                    for user_id in user_ids:
                        for context_id in context_ids:
                            super().get_or_create(user_id=user_id, location_id=context_id)

        return data

    def updateFromRequest(self, request, removed=None, function=None):
        if not isinstance(request, DSRequest):
            request = DSRequest(request=request)
        data = request.get_data()
        parent_id = data.get('parent_id')

        with transaction.atomic():
            props = data.get('props')
            if data.get('compulsory_reading') == True:
                props |= Locations_users.props.compulsory_reading
            else:
                props &= ~Locations_users.props.compulsory_reading

            if data.get('resiver_production_order') == True:
                props |= Locations_users.props.resiver_production_order
            else:
                props &= ~Locations_users.props.resiver_production_order

            _data = dict()
            setAttr(_data, 'props', props)
            setAttr(_data, 'parent_id', parent_id)

            super().update_or_create(id=data.get('id'), defaults=_data)

            return data

    def copyUsersFromRequest(self, request, removed=None, function=None):
        if not isinstance(request, DSRequest):
            request = DSRequest(request=request)
        data = request.get_data()
        source = data.get('source')
        destination = data.get('destination')

        res = 0
        with transaction.atomic():
            for s in source:
                Locations_users.objects.get_or_create(user_id=s.get('user_id'), location_id=s.get('context_id'), parent_id=destination.get('user_id'))
                res += 1
            return res

    def deleteFromRequest(self, request, removed=None, ):
        request = DSRequest(request=request)
        res = 0
        tuple_ids = request.get_tuple_ids()
        with transaction.atomic():
            for id, mode in tuple_ids:
                if mode == 'hide':
                    super().filter(id=id).soft_delete()
                elif mode == 'visible':
                    super().filter(id=id).soft_restore()
                else:
                    super().filter(id=id).delete()
                    res += 1

            return res

    @classmethod
    def getRecord(cls, record):
        res = {
            'compulsory_reading': record.props.compulsory_reading,
            'deliting': record.deliting,
            'editing': record.editing,
            'id': record.id,
            'location_id': record.location.id,
            'location_position': record.location_position,
            'parent_id': record.parent.id if record.parent else None,
            'props': record.props,
            'resiver_production_order': record.props.resiver_production_order,
            'user__email': record.user.email,
            'user__first_name': record.user.first_name,
            'user__last_name': record.user.last_name,
            'user__middle_name': record.user.middle_name,
            'user__username': record.user.username,
            'user_id': record.user.id,
        }
        return DelProps(res)

    @classmethod
    def getRecord1(cls, record):
        res = {
            'location_id': record.location.id,
        }
        return DelProps(res)

    def get_queryset(self):
        return Locations_usersQuerySet(self.model, using=self._db)


class Locations_users(Hierarcy):
    location = ForeignKeyCascade(Locations)
    user = ForeignKeyCascade(User)
    props = BitField(flags=(
        ('compulsory_reading', 'Обязательное прочтение'),  # 1
        ('resiver_production_order', 'Прием заказав на производство, на верхнем уровне'),  # 1
    ), default=0, db_index=True)

    @property
    def location_position(self):
        from kaf_pas.input.models.user_add_info import User_add_info
        res = []
        for item in User_add_info.objects.filter(user=self.user):
            res.append(f'{item.location.full_name} : {item.position.name}')
        return ', '.join(res)

    @classmethod
    def user_location_ids(cls, user):
        if isinstance(user, int):
            return list(set(map(lambda x: x.location.id, cls.objects.filter(user_id=user))))
        elif isinstance(user, User):
            return list(set(map(lambda x: x.location.id, cls.objects.filter(user=user))))
        elif isinstance(user, list):
            return list(set(map(lambda x: x.location.id, cls.objects.filter(user_id__in=user))))
        else:
            raise Exception(f'{user} must be int or User')

    @classmethod
    def location_user_ids(cls, location):
        if isinstance(location, int):
            return list(set(map(lambda x: x.user.id, cls.objects.filter(location_id=location))))
        elif isinstance(location, Locations):
            return list(set(map(lambda x: x.user.id, cls.objects.filter(location=location))))
        elif isinstance(location, list):
            return list(set(map(lambda x: x.user.id, cls.objects.filter(location_id__in=location))))
        else:
            raise Exception(f'{location} must be int or Locations')

    objects = Locations_usersManager()

    def __str__(self):
        return f"ID:{self.id}, location: [{self.location}], user: [{self.user}]"

    class Meta:
        constraints = [
            UniqueConstraint(fields=['location', 'user'], condition=Q(parent=None), name='Locations_users_unique_constraint_0'),
            UniqueConstraint(fields=['location', 'parent', 'user'], name='Locations_users_unique_constraint_1'),
        ]
        verbose_name = 'Ответственные пользователи ресурсов'
