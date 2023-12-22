import graphene

from graphene_django import DjangoObjectType
from core import ExtendedConnection
from business_config.models import BusinessConfig


class BusinessConfigGQLType(DjangoObjectType):
    uuid = graphene.String(source='uuid')

    class Meta:
        model = BusinessConfig
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            "id": ["exact"],

            "key": ["exact", "iexact", "istartswith", "icontains"],
            "value": ["exact", "iexact", "istartswith", "icontains"],
            "date_valid_from": ["exact", "lt", "lte", "gt", "gte"],
            "date_valid_to": ["exact", "lt", "lte", "gt", "gte"],

            "date_created": ["exact", "lt", "lte", "gt", "gte"],
            "date_updated": ["exact", "lt", "lte", "gt", "gte"],
            "is_deleted": ["exact"],
            "version": ["exact"],
        }
        connection_class = ExtendedConnection
