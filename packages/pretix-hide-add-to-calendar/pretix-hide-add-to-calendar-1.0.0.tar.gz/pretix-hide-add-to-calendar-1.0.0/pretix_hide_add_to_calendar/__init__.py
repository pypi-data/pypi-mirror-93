from django.utils.translation import gettext_lazy

try:
    from pretix.base.plugins import PluginConfig
except ImportError:
    raise RuntimeError("Please use pretix 2.7 or above to run this plugin!")

__version__ = "1.0.0"


class PluginApp(PluginConfig):
    name = "pretix_hide_add_to_calendar"
    verbose_name = 'Hide "Add to calendar"'

    class PretixPluginMeta:
        name = gettext_lazy('Hide "Add to calendar"')
        author = "RM"
        description = gettext_lazy('Hide "Add to calendar" link')
        visible = True
        version = __version__
        category = "CUSTOMIZATION"
        compatibility = "pretix>=3.0.0"

    def ready(self):
        from . import signals  # NOQA


default_app_config = "pretix_hide_add_to_calendar.PluginApp"
