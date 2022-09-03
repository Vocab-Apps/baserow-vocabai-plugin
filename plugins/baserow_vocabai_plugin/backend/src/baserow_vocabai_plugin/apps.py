from baserow.core.registries import plugin_registry
from django.apps import AppConfig


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
