from django.db.models import Q
from business_config.models import BusinessConfig
from core.validation import BaseModelValidation


class ValidationException(Exception):
    pass


class BusinessConfigValidation(BaseModelValidation):
    OBJECT_TYPE = BusinessConfig

    @classmethod
    def validate_create(cls, user, **data):
        cls._check_date_range_overlap(**data)

    @classmethod
    def validate_update(cls, user, **data):
        cls._check_date_range_overlap(**data)

    @staticmethod
    def _check_date_range_overlap(**data):
        # Date range overlap
        filters = [Q(date_valid_from__date__lte=data.get('date_valid_to'),
                     date_valid_to__date__gte=data.get('date_valid_from'))]

        # skip current record on update
        obj_id = data.get('id', None)
        if obj_id:
            filters.append(~Q(id=obj_id))

        if BusinessConfig.objects.filter(*filters).exists():
            raise ValidationException("business_config.validation.date_range_overlap")
