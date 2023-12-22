from django.test import TestCase
from graphene import Schema
from graphene.test import Client

from business_config.models import BusinessConfig
from business_config.schema import Query, Mutation
from business_config.tests.data.gql_payload import gql_query_payload, gql_create_payload, gql_update_payload, \
    gql_delete_payload, mutation_id
from core import datetime
from core.models import Role, MutationLog
from core.test_helpers import create_test_interactive_user


class BusinessConfigGQLTestCase(TestCase):
    class GQLContext:
        def __init__(self, user):
            self.user = user

    user = None
    service = None

    gql_client = None
    gql_context = None

    @classmethod
    def setUpClass(cls):
        super(BusinessConfigGQLTestCase, cls).setUpClass()
        role_admin = Role.objects.get(name='IMIS Administrator', validity_to__isnull=True)

        cls.user = create_test_interactive_user(username='VoucherTestUser1', roles=[role_admin.id])

        gql_schema = Schema(
            query=Query,
            mutation=Mutation
        )

        cls.gql_client = Client(gql_schema)
        cls.gql_context = cls.GQLContext(cls.user)

    def test_query(self):
        _ = self._create_business_config()
        res = self.gql_client.execute(gql_query_payload, context=self.gql_context)
        self.assertFalse(res.get('errors', False), res.get('errors'))
        self.assertTrue(res.get('data', {}).get('businessConfig', {}).get('edges', {}))

    def test_create(self):
        res = self.gql_client.execute(gql_create_payload, context=self.gql_context)
        self.assertFalse(res.get('errors', False), res.get('errors'))
        mutation_log = MutationLog.objects.get(client_mutation_id=mutation_id)
        self.assertFalse(mutation_log.error)
        self.assertEquals(BusinessConfig.objects.filter(is_deleted=False).count(), 1)

    def test_update(self):
        id = self._create_business_config()
        res = self.gql_client.execute(gql_update_payload, context=self.gql_context, variables={"id": id})
        self.assertFalse(res.get('errors', False), res.get('errors'))
        mutation_log = MutationLog.objects.get(client_mutation_id=mutation_id)
        self.assertFalse(mutation_log.error)
        self.assertEquals(BusinessConfig.objects.filter(is_deleted=False, version=2).count(), 1)

    def test_delete(self):
        id = self._create_business_config()
        res = self.gql_client.execute(gql_delete_payload, context=self.gql_context, variables={"id": id})
        self.assertFalse(res.get('errors', False), res.get('errors'))
        mutation_log = MutationLog.objects.get(client_mutation_id=mutation_id)
        self.assertFalse(mutation_log.error)
        self.assertEquals(BusinessConfig.objects.filter(is_deleted=True).count(), 1)

    def _create_business_config(self):
        today = datetime.date.today()
        yesterday = today - datetime.datetimedelta(days=1)
        tomorrow = today + datetime.datetimedelta(days=1)

        obj = BusinessConfig(**{
            'key': 'key1',
            'value': 'value1',
            'date_valid_from': str(yesterday),
            'date_valid_to': str(tomorrow),
        })
        obj.save(username=self.user.username)
        return obj.id
