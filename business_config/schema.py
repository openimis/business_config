import graphene
import graphene_django_optimizer as gql_optimizer
from django.db.models import Q
from django.contrib.auth.models import AnonymousUser
from django.utils.translation import gettext as _

from business_config.gql_mutations import CreateBusinessConfigMutation, DeleteBusinessConfigMutation, \
    UpdateBusinessConfigMutation
from business_config.services import get_current_config_field_filter
from core import datetime
from core.schema import OrderedDjangoFilterConnectionField
from business_config.models import BusinessConfig
from business_config.gql_queries import BusinessConfigGQLType
from core.utils import append_validity_filter


class Query(graphene.ObjectType):
    module_name = "business_config"

    business_config = OrderedDjangoFilterConnectionField(
        BusinessConfigGQLType,
        orderBy=graphene.List(of_type=graphene.String),
        client_mutation_id=graphene.String(),
    )

    current_business_config = OrderedDjangoFilterConnectionField(
        BusinessConfigGQLType,
        date=graphene.Date()
    )

    def resolve_business_config(self, info, client_mutation_id=None, **kwargs):
        query = BusinessConfig.objects

        filters = append_validity_filter(**kwargs)

        if client_mutation_id:
            filters.append(Q(mutations__mutation__client_mutation_id=client_mutation_id))

        return gql_optimizer.query(query.filter(*filters), info)

    def resolve_current_business_config(self, info, key=None, date=None, **kwargs):
        query = BusinessConfig.objects

        if not key:
            raise AttributeError("business_config.validation.key_required")

        filters = append_validity_filter(**kwargs)
        filters += get_current_config_field_filter(key, date or datetime.date.today())

        return gql_optimizer.query(query.filter(*filters), info)

    @staticmethod
    def _check_permissions(user, perms):
        if type(user) is AnonymousUser or not user.id or not user.has_perms(perms):
            raise PermissionError(_("Unauthorized"))


class Mutation(graphene.ObjectType):
    create_business_config = CreateBusinessConfigMutation.Field()
    update_business_config = UpdateBusinessConfigMutation.Field()
    delete_business_config = DeleteBusinessConfigMutation.Field()
