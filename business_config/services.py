import logging
from django.db.models import Q
from business_config.models import BusinessConfig
from business_config.validation import BusinessConfigValidation
from core import datetime
from core.services import BaseService
from core.signals import register_service_signal

logger = logging.getLogger(__name__)


class BusinessConfigService(BaseService):
    OBJECT_TYPE = BusinessConfig

    def __init__(self, user, validation_class=BusinessConfigValidation):
        super().__init__(user, validation_class)

    @register_service_signal('business_config_service.create')
    def create(self, obj_data):
        return super().create(obj_data)

    @register_service_signal('business_config_service.update')
    def update(self, obj_data):
        return super().update(obj_data)

    @register_service_signal('business_config_service.delete')
    def delete(self, obj_data):
        return super().delete(obj_data)


def get_current_config_field_filter(key: str, date: datetime.date) -> [Q]:
    return [Q(
        date_valid_from__date__lte=date,
        date_valid_to__date__gte=date,
        key=key,
        is_deleted=False
    )]
