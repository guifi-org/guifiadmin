from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ProvidersConfig(AppConfig):
    name = 'providers'
    verbose_name = _('Providers')
