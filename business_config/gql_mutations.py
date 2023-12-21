import graphene as graphene
from django.db import transaction
from pydantic.error_wrappers import ValidationError
from django.contrib.auth.models import AnonymousUser

from business_config.apps import BusinessConfigConfig
from business_config.models import BusinessConfig
from business_config.services import BusinessConfigService
from core.gql.gql_mutations.base_mutation import BaseMutation
from core.schema import OpenIMISMutation


class CreateBusinessConfigInput(OpenIMISMutation.Input):
    key = graphene.String(max_length=255, required=True)
    value = graphene.String(max_length=255, required=True)
    date_valid_from = graphene.Date(required=True)
    date_valid_to = graphene.Date(required=True)


class UpdateBusinessConfigInput(OpenIMISMutation.Input):
    id = graphene.ID(required=True)
    key = graphene.String(max_length=255)
    value = graphene.String(max_length=255)
    date_valid_from = graphene.Date()
    date_valid_to = graphene.Date()


class DeleteBusinessConfigInput(OpenIMISMutation.Input):
    ids = graphene.List(graphene.ID, required=True)


class CreateBusinessConfigMutation(BaseMutation):
    _mutation_class = "CreateBusinessConfigMutation"
    _mutation_module = "business_config"
    _model = BusinessConfig

    @classmethod
    def _validate_mutation(cls, user, **data):
        if type(user) is AnonymousUser or not user.id or not user.has_perms(
                BusinessConfigConfig.gql_business_config_create_perms):
            raise ValidationError("mutation.authentication_required")

    @classmethod
    def _mutate(cls, user, **data):
        data.pop('client_mutation_id', None)
        data.pop('client_mutation_label', None)

        service = BusinessConfigService(user)
        response = service.create(data)
        if not response['success']:
            return response
        return None

    class Input(CreateBusinessConfigInput):
        pass


class UpdateBusinessConfigMutation(BaseMutation):
    _mutation_class = "UpdateBusinessConfigMutation"
    _mutation_module = "business_config"
    _model = BusinessConfig

    @classmethod
    def _validate_mutation(cls, user, **data):
        if type(user) is AnonymousUser or not user.id or not user.has_perms(
                BusinessConfigConfig.gql_business_config_update_perms):
            raise ValidationError("mutation.authentication_required")

    @classmethod
    def _mutate(cls, user, **data):
        data.pop('client_mutation_id', None)
        data.pop('client_mutation_label', None)

        service = BusinessConfigService(user)
        response = service.update(data)
        if not response['success']:
            return response
        return None

    class Input(UpdateBusinessConfigInput):
        pass


class DeleteBusinessConfigMutation(BaseMutation):
    _mutation_class = "DeleteBusinessConfigMutation"
    _mutation_module = "business_config"
    _model = BusinessConfig

    @classmethod
    def _validate_mutation(cls, user, **data):
        if type(user) is AnonymousUser or not user.id or not user.has_perms(
                BusinessConfigConfig.gql_business_config_delete_perms):
            raise ValidationError("mutation.authentication_required")

    @classmethod
    def _mutate(cls, user, **data):
        data.pop('client_mutation_id', None)
        data.pop('client_mutation_label', None)

        service = BusinessConfigService(user)
        ids = data.get('ids')
        if ids:
            with transaction.atomic():
                for id in ids:
                    res = service.delete({'id': id})
                    if not res.get('success', False):
                        raise ValueError(f"{res.get('message')}: {res.get('detail')}")

    class Input(DeleteBusinessConfigInput):
        pass
