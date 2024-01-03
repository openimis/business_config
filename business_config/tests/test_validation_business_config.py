from django.test import TestCase

from business_config.models import BusinessConfig
from business_config.services import BusinessConfigService
from business_config.tests.data.service_payload import service_create_payload, service_update_payload, yesterday, \
    tomorrow
from business_config.validation import ValidationException
from core.models import Role
from core import datetime
from core.test_helpers import create_test_interactive_user


class BusinessConfigValidationTestCase(TestCase):
    user = None
    service = None
    validation = None

    delta_3_days = None

    @classmethod
    def setUpClass(cls):
        super(BusinessConfigValidationTestCase, cls).setUpClass()
        role_admin = Role.objects.get(name='IMIS Administrator', validity_to__isnull=True)

        cls.user = create_test_interactive_user(username='VoucherTestUser1', roles=[role_admin.id])
        cls.service = BusinessConfigService(cls.user.i_user)
        cls.validation = cls.service.validation_class
        cls.delta_3_days = datetime.datetimedelta(days=3)

    def test_valid_create(self):
        self._create_config()
        payload = {**service_create_payload, 'date_valid_from': yesterday + self.delta_3_days,
                   'date_valid_to': tomorrow + self.delta_3_days}

        try:
            self.validation.validate_create(self.user, **payload)
        except ValidationException as e:
            self.fail(f"Validation failed: {e}")

    def test_invalid_create_dates_overlap(self):
        self._create_config()
        payload = {**service_create_payload, 'date_valid_from': tomorrow,
                   'date_valid_to': tomorrow + self.delta_3_days}

        self.assertRaises(ValidationException, lambda: self.validation.validate_create(self.user, **payload))

    def test_valid_update(self):
        self._create_config(date_valid_from=yesterday, date_valid_to=tomorrow)
        payload = {**service_create_payload, 'date_valid_from': yesterday + self.delta_3_days,
                   'date_valid_to': tomorrow + self.delta_3_days}

        try:
            self.validation.validate_update(self.user, **payload)
        except ValidationException as e:
            self.fail(f"Validation failed: {e}")

    def test_valid_update_self_overlap(self):
        data = self._create_config(date_valid_from=yesterday, date_valid_to=tomorrow)
        payload = {**service_create_payload, 'date_valid_from': tomorrow,
                   'date_valid_to': tomorrow + self.delta_3_days, 'id': data.get('id')}

        try:
            self.validation.validate_update(self.user, **payload)
        except ValidationException as e:
            self.fail(f"Validation failed: {e}")

    def test_invalid_update_dates_overlap(self):
        self._create_config(date_valid_from=yesterday, date_valid_to=tomorrow)
        data = self._create_config(date_valid_from=yesterday + self.delta_3_days,
                                   date_valid_to=tomorrow + self.delta_3_days)

        payload = {**service_create_payload, 'date_valid_from': tomorrow,
                   'date_valid_to': tomorrow + self.delta_3_days, 'id': data.get('id')}

        self.assertRaises(ValidationException, lambda: self.validation.validate_update(self.user, **payload))

    def _create_config(self, **data):
        res = self.service.create({**service_create_payload, **data})
        self.assertTrue(res.get('success', False), res.get('detail'))
        return res.get('data', {})
