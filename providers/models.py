# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Invoice(models.Model):
    title = models.CharField(_("title"), max_length=200)
    date = models.DateField(_("date"), default=now)
    invoice_number = models.CharField(_("invoice number"), max_length=50)
    provider = models.ForeignKey('accounting.Person', related_name="providers_invoices", verbose_name=_("provider"), on_delete=models.CASCADE)
    total = models.DecimalField(_("total"), max_digits=9, decimal_places=2)
    notes = models.TextField(_("notes"), blank=True, null=True)

    class Meta:
        verbose_name = _("invoice")
        verbose_name_plural = _("invoices")

    def __str__(self):
        return self.invoice_number
