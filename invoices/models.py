# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now

from smart_selects.db_fields import ChainedForeignKey

from . import invoice_settings


@python_2_unicode_compatible
class VAT(models.Model):
    percent = models.IntegerField(_("percent"))

    class Meta:
        verbose_name = _("VAT")
        verbose_name_plural = _("VATs")

    def __str__(self):
        return str(self.percent)


def default_vat():
    return VAT.objects.first()


@python_2_unicode_compatible
class Estimate(models.Model):
    title = models.CharField(_("title"), max_length=200)
    date = models.DateField(_("date"), default=now)
    person = models.ForeignKey('accounting.Person', verbose_name=_("person"), on_delete=models.CASCADE)
    address = ChainedForeignKey("geolocation.Address", verbose_name=_("address"), on_delete=models.CASCADE, blank=True, null=True,
                                chained_field="person", chained_model_field="person", show_all=False, auto_choose=True)
    total = models.DecimalField(_("total"), max_digits=9, decimal_places=2)
    notes = models.TextField(_("notes"), blank=True, null=True)

    class Meta:
        verbose_name = _("estimate")
        verbose_name_plural = _("estimates")

    def __str__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('estimate_detail', (), {'estimate_pk': self.pk})

    def save(self, *args, **kwargs):
        self.update_total()
        super(Estimate, self).save(*args, **kwargs)

    def update_total(self):
        self.total = self.lines.aggregate(total=models.Sum('total'))['total']
        if self.total is None:
            self.total = 0

    def vat_details(self):
        taxes = self.lines.values('vat__percent').annotate(total=models.Sum('total'))
        for tax in taxes:
            tax['base'] = tax['total'] * 100 / (100 + tax['vat__percent'])
            tax['tax'] = tax['total'] - tax['base']
        return taxes

    def convert_to_invoice(self):
        invoice = Invoice.objects.create(
            person=self.person,
            notes=self.notes,
            estimate=self,
        )
        for line in self.lines.all():
            InvoiceLine.objects.create(
                invoice=invoice,
                description=line.description,
                vat=line.vat,
                quantity=line.quantity,
                unit_price=line.unit_price,
            )
        invoice.save()
        return invoice


@python_2_unicode_compatible
class EstimateLine(models.Model):
    estimate = models.ForeignKey(Estimate, verbose_name=_("estimate"), related_name='lines', on_delete=models.CASCADE)
    description = models.CharField(_("description"), max_length=250)
    vat = models.ForeignKey(VAT, verbose_name=_("vat"), default=default_vat, on_delete=models.CASCADE)
    quantity = models.IntegerField(_("quantity"), default=1)
    unit_price = models.DecimalField(_("unit price"), max_digits=9, decimal_places=2)
    total = models.DecimalField(_("total"), max_digits=9, decimal_places=2)

    class Meta:
        verbose_name = _("estimate line")
        verbose_name_plural = _("estimate lines")

    def __str__(self):
        return "{}: {}".format(self.estimate, self.description)

    def save(self, *args, **kwargs):
        self.total = self.unit_price * self.quantity * (1 + Decimal(self.vat.percent) / 100)
        super(EstimateLine, self).save(*args, **kwargs)


@python_2_unicode_compatible
class Invoice(models.Model):
    date = models.DateField(_("date"), default=now)
    number = models.IntegerField(_("number"), unique=True)
    person = models.ForeignKey('accounting.Person', verbose_name=_("person"), on_delete=models.CASCADE)
    # address = models.ForeignKey("geolocation.Address", verbose_name=_("address"), on_delete=models.CASCADE, blank=True, null=True)
    address = ChainedForeignKey("geolocation.Address", verbose_name=_("address"), on_delete=models.CASCADE, blank=True, null=True,
                                chained_field="person", chained_model_field="person", show_all=False, auto_choose=True)
    total = models.DecimalField(_("total"), max_digits=9, decimal_places=2)
    notes = models.TextField(_("notes"), blank=True, null=True)
    estimate = models.ForeignKey(Estimate, verbose_name=_("estimate"), blank=True, null=True, on_delete=models.SET_NULL)
    is_paid = models.BooleanField(_('is paid'), default=False)

    class Meta:
        verbose_name = _("invoice")
        verbose_name_plural = _("invoices")

    @property
    def invoice_number(self):
        return "{}-{:05}".format(invoice_settings.INVOICE_PREFIX, self.number)

    def __str__(self):
        return self.invoice_number

    @models.permalink
    def get_absolute_url(self):
        return ('invoice_detail', (), {'invoice': self.number})

    def save(self, *args, **kwargs):
        self.update_total()

        if self.number is None:
            number = Invoice.objects.aggregate(last=models.Max('number'))['last']
            if not number:
                number = 0
            self.number = number + 1

        super(Invoice, self).save(*args, **kwargs)

    def update_total(self):
        self.total = self.lines.aggregate(total=models.Sum('total'))['total']
        if self.total is None:
            self.total = 0

    def vat_details(self):
        taxes = self.lines.values('vat__percent').annotate(total=models.Sum('total'))
        for tax in taxes:
            tax['base'] = tax['total'] * 100 / (100 + tax['vat__percent'])
            tax['tax'] = tax['total'] - tax['base']
        return taxes


@python_2_unicode_compatible
class InvoiceLine(models.Model):
    invoice = models.ForeignKey(Invoice, verbose_name=_("invoice"), related_name='lines', on_delete=models.CASCADE)
    description = models.CharField(_("description"), max_length=250)
    vat = models.ForeignKey(VAT, verbose_name=_("vat"), default=default_vat, on_delete=models.CASCADE)
    quantity = models.IntegerField(_("quantity"), default=1)
    unit_price = models.DecimalField(_("unit price"), max_digits=9, decimal_places=2)
    total = models.DecimalField(_("total"), max_digits=9, decimal_places=2)

    class Meta:
        verbose_name = _("invoice line")
        verbose_name_plural = _("invoice lines")

    def __str__(self):
        return "{}: {}".format(self.invoice.number, self.description)

    def save(self, *args, **kwargs):
        self.total = self.unit_price * self.quantity * (1 + Decimal(self.vat.percent) / 100)
        super(InvoiceLine, self).save(*args, **kwargs)
