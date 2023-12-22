import logging

from business_config.models import BusinessConfig
from business_config.validation import BusinessConfigValidation
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
