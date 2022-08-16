from baserow.core.registries import plugin_registry
from django.apps import AppConfig


class PluginNameConfig(AppConfig):
    name = "baserow_vocabai_plugin"

    def ready(self):
        from .plugins import PluginNamePlugin

        plugin_registry.register(PluginNamePlugin())
