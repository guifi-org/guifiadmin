# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class InvoicesConfig(AppConfig):
    name = 'invoices'
    verbose_name = _('Invoices')

    def ready(self):
        from . import signals  # NOQA
