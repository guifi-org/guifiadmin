from django.apps import AppConfig


class GuifiConfig(AppConfig):
    name = 'guifi'
    verbose_name = 'Guifi.net'

    def ready(self):
        from . import signals  # NOQA
