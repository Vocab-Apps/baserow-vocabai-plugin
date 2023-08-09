import sys

def setup(settings):
    """
    This function is called after Baserow as setup its own Django settings file but
    before Django starts. Read and modify provided settings object as appropriate
    just like you would in a normal Django settings file. E.g.:

    settings.INSTALLED_APPS += ["some_custom_plugin_dep"]
    for db, value in settings.DATABASES:
        value['engine'] = 'some custom engine'
    """

    # prior to baserow 1.19.1, the following fix was required
    # see here: https://community.baserow.io/t/when-running-pytest-on-a-plugin-runtimeerror-model-class-baserow-contrib-builder-pages-models-page-doesnt-declare-an-explicit-app-label-and-isnt-in-an-application-in-installed-apps/2548/2
    # if "pytest" in sys.modules:
    #     settings.INSTALLED_APPS += ["baserow.contrib.builder"]