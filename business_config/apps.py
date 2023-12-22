from django.apps import AppConfig

DEFAULT_CONFIG = {
    "gql_business_config_search_perms": ["205001"],
    "gql_business_config_create_perms": ["205002"],
    "gql_business_config_update_perms": ["205003"],
    "gql_business_config_delete_perms": ["205004"],
}


class BusinessConfigConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'business_config'

    gql_business_config_search_perms = None
    gql_business_config_create_perms = None
    gql_business_config_update_perms = None
    gql_business_config_delete_perms = None

    def ready(self):
        from core.models import ModuleConfiguration

        cfg = ModuleConfiguration.get_or_default(self.name, DEFAULT_CONFIG)
        self._load_config(cfg)

    @classmethod
    def _load_config(cls, cfg):
        """
        Load all config fields that match current AppConfig class fields, all custom fields have to be loaded separately
        """
        for field in cfg:
            if hasattr(cls, field):
                setattr(cls, field, cfg[field])
