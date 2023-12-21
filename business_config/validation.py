from business_config.models import BusinessConfig
from core.validation import BaseModelValidation


class BusinessConfigValidation(BaseModelValidation):
    OBJECT_TYPE = BusinessConfig

    @classmethod
    def validate_create(cls, user, **data):
        pass

    @classmethod
    def validate_update(cls, user, **data):
        pass
