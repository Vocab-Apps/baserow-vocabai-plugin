from baserow.core.registries import plugin_registry
from django.apps import AppConfig

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://f7a7fa7dfe5f412f852c3bfe2defa091@o968582.ingest.sentry.io/6742581",
    integrations=[
        DjangoIntegration(),
    ],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

class PluginNameConfig(AppConfig):
    name = "baserow_vocabai_plugin"

    def ready(self):
        from .plugins import PluginNamePlugin

        plugin_registry.register(PluginNamePlugin())

        from baserow.contrib.database.fields.registries import field_type_registry

        from .fields.vocabai_fieldtypes import LanguageFieldType, TranslationFieldType, TransliterationFieldType, DictionaryLookupFieldType        

        field_type_registry.register(LanguageFieldType())
        field_type_registry.register(TranslationFieldType())
        field_type_registry.register(TransliterationFieldType())
        field_type_registry.register(DictionaryLookupFieldType())
