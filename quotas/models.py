# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import make_aware, utc
from django.utils.translation import ugettext_lazy as _

from invoices.models import Invoice


@python_2_unicode_compatible
class QuotaType(models.Model):
    ANUAL = 1
    MONTHLY = 2
    PERIODICITY_CHOICES = (
        (ANUAL, _("anual")),
        (MONTHLY, _("monthly")),
    )
    periodicity = models.PositiveSmallIntegerField(_("periodicity"), choices=PERIODICITY_CHOICES)
    quantity = models.DecimalField(_("quantity"), max_digits=9, decimal_places=2)
    description = models.CharField(_("description"), max_length=250)

    class Meta:
        verbose_name = _("quota type")
        verbose_name_plural = _("quota types")

    def __str__(self):
        return self.description


class QuotaQuerySet(models.QuerySet):
    def create_invoices(self, date):
        # monthly quotas
        start = make_aware(datetime.datetime(date.year, date.month, 1), utc)
        if date.month == 12:
            year = date.year + 1
            month = 1
        else:
            year = date.year
            month = date.month + 1
        end = make_aware(datetime.datetime(year, month, 1), utc)
        for quota in self.filter(quota_type__periodicity=QuotaType.MONTHLY):
            if not quota.quotainvoice_set.filter(date__range=(start, end)).exists():
                print "quota necesita invoice:", quota.create_invoice(date)

        # yearly quotas
        start = make_aware(datetime.datetime(date.year, 1, 1), utc)
        end = make_aware(datetime.datetime(date.year + 1, 1, 1), utc)

        quotainvoices = []
        for quota in self.filter(quota_type__periodicity=QuotaType.ANUAL):
            if not quota.quotainvoice_set.filter(date__range=(start, end)).exists():
                quotainvoice = quota.create_invoice(date)
                quotainvoices.append(quotainvoice)
        return quotainvoices


@python_2_unicode_compatible
class Quota(models.Model):
    member = models.ForeignKey('accounting.Member', verbose_name=_("member"), on_delete=models.CASCADE)
    quota_type = models.ForeignKey(QuotaType, verbose_name=_("quota type"), on_delete=models.CASCADE)

    objects = QuotaQuerySet.as_manager()

    class Meta:
        verbose_name = _("quota")
        verbose_name_plural = _("quotas")

    def __str__(self):
        return "{}:{}".format(self.member.username, self.quota_type)

    def create_invoice(self, date):
        invoice = Invoice.objects.create(
            date=date,
            person=self.member.person,
        )
        description = self.quota_type.description
        if self.quota_type.periodicity == QuotaType.ANUAL:
            description = "{0}: {1}".format(description, date.year)
        elif self.quota_type.periodicity == QuotaType.MONTHLY:
            description = "{0}: {1}".format(description, date.strftime("%Y-%m"))
        invoice.lines.create(
            description=description,
            quantity=1,
            unit_price=self.quota_type.quantity,
        )
        invoice.save()  # update invoice total
        quotainvoice = QuotaInvoice.objects.create(date=date, invoice=invoice, quota=self)
        return quotainvoice


@python_2_unicode_compatible
class QuotaInvoice(models.Model):
    date = models.DateTimeField(_("date"))
    invoice = models.ForeignKey(Invoice, verbose_name=_("invoice"), on_delete=models.CASCADE)
    quota = models.ForeignKey(Quota, verbose_name=_("quota type"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("quota invoice")
        verbose_name_plural = _("quota invoices")

    def __str__(self):
        return "{}:{}".format(self.quota, self.date)
