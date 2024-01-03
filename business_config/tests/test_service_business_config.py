from django.test import TestCase

from business_config.models import BusinessConfig
from business_config.services import BusinessConfigService
from business_config.tests.data.service_payload import service_create_payload, service_update_payload
from core.models import Role
from core.test_helpers import create_test_interactive_user


class BusinessConfigServiceTestCase(TestCase):
    user = None
    service = None

    @classmethod
    def setUpClass(cls):
        super(BusinessConfigServiceTestCase, cls).setUpClass()
        role_admin = Role.objects.get(name='IMIS Administrator', validity_to__isnull=True)

        cls.user = create_test_interactive_user(username='VoucherTestUser1', roles=[role_admin.id])
        cls.service = BusinessConfigService(cls.user.i_user)

    def test_create(self):
        res = self.service.create(service_create_payload)

        self.assertTrue(res.get('success', False), res.get("detail", "Unknown error"))
        self.assertEquals(BusinessConfig.objects.filter(is_deleted=False).count(), 1)

    def test_update(self):
        res = self.service.create(service_create_payload)
        self.assertTrue(res.get('success', False), res.get("detail", "Unknown error"))
        self.assertEquals(BusinessConfig.objects.filter(is_deleted=False).count(), 1)

        res = self.service.update({**service_update_payload, **{'id': res.get("data", {}).get("id", None)}})

        self.assertTrue(res.get('success', False), res.get("detail", "Unknown error"))
        self.assertEquals(BusinessConfig.objects.filter(is_deleted=False).count(), 1)

    def test_delete(self):
        res = self.service.create(service_create_payload)
        self.assertTrue(res.get('success', False), res.get("detail", "Unknown error"))
        self.assertEquals(BusinessConfig.objects.filter(is_deleted=False).count(), 1)

        res = self.service.delete({'id': res.get("data", {}).get("id", None)})
        self.assertTrue(res.get('success', False), res.get("detail", "Unknown error"))
        self.assertEquals(BusinessConfig.objects.filter(is_deleted=True).count(), 1)
