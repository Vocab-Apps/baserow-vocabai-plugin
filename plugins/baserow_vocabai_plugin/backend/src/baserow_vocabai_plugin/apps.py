from baserow.core.registries import plugin_registry
from baserow.contrib.database.fields.registries import field_type_registry
from django.apps import AppConfig


from .fields.vocabai_fieldtypes import LanguageFieldType, TranslationFieldType, TransliterationFieldType, DictionaryLookupFieldType

class PluginNameConfig(AppConfig):
    name = "baserow_vocabai_plugin"

    def ready(self):
        from .plugins import PluginNamePlugin

        plugin_registry.register(PluginNamePlugin())

        field_type_registry.register(LanguageFieldType())
        field_type_registry.register(TranslationFieldType())
        field_type_registry.register(TransliterationFieldType())
        field_type_registry.register(DictionaryLookupFieldType())
