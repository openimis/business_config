from django.test import TestCase
from graphene import Schema
from graphene.test import Client

from business_config.models import BusinessConfig
from business_config.schema import Query, Mutation
from business_config.tests.data.gql_payload import gql_query_payload_current, gql_query_payload_date
from core import datetime
from core.models import Role
from core.test_helpers import create_test_interactive_user


class CurrentBusinessConfigGQLTestCase(TestCase):
    class GQLContext:
        def __init__(self, user):
            self.user = user

    user = None
    service = None

    gql_client = None
    gql_context = None

    today = None
    yesterday = None
    tomorrow = None

    @classmethod
    def setUpClass(cls):
        super(CurrentBusinessConfigGQLTestCase, cls).setUpClass()
        role_admin = Role.objects.get(name='IMIS Administrator', validity_to__isnull=True)

        cls.user = create_test_interactive_user(username='VoucherTestUser1', roles=[role_admin.id])

        cls.today = datetime.date.today()
        cls.yesterday = cls.today - datetime.datetimedelta(days=1)
        cls.tomorrow = cls.today + datetime.datetimedelta(days=1)

        gql_schema = Schema(
            query=Query,
            mutation=Mutation
        )

        cls.gql_client = Client(gql_schema)
        cls.gql_context = cls.GQLContext(cls.user)

    def test_query(self):
        _ = self._create_business_config()
        res = self.gql_client.execute(gql_query_payload_current, context=self.gql_context)
        self.assertFalse(res.get('errors', False), res.get('errors'))
        self.assertTrue(res.get('data', {}).get('currentBusinessConfig', {}).get('edges', {}))

    def test_query_date(self):
        _ = self._create_business_config()
        res = self.gql_client.execute(gql_query_payload_date, context=self.gql_context,
                                      variables={'date': str(self.tomorrow)})
        self.assertFalse(res.get('errors', False), res.get('errors'))
        self.assertTrue(res.get('data', {}).get('currentBusinessConfig', {}).get('edges', {}))

    def test_query_date_empty(self):
        _ = self._create_business_config()
        res = self.gql_client.execute(gql_query_payload_date, context=self.gql_context,
                                      variables={'date': str(self.today + datetime.datetimedelta(days=3))})
        self.assertFalse(res.get('errors', False), res.get('errors'))
        self.assertFalse(res.get('data', {}).get('currentBusinessConfig', {}).get('edges', {}))

    def _create_business_config(self, **kwargs):
        today = datetime.date.today()
        yesterday = today - datetime.datetimedelta(days=1)
        tomorrow = today + datetime.datetimedelta(days=1)

        obj = BusinessConfig(**{
            'key': 'key1',
            'value': 'value1',
            'date_valid_from': str(yesterday),
            'date_valid_to': str(tomorrow),
            **kwargs
        })
        obj.save(username=self.user.username)
        return obj.id
