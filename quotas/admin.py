# -*- coding: utf-8 -*-
import datetime

from django.contrib import admin
from django.db.models import Max
from django.utils.timezone import now, make_aware, utc
from django.utils.translation import ugettext_lazy as _

from . import models


@admin.register(models.QuotaType)
class QuotaTypeAdmin(admin.ModelAdmin):
    list_display = ('periodicity', 'description', 'quantity')
    list_filter = ('periodicity', )


@admin.register(models.Quota)
class QuotaAdmin(admin.ModelAdmin):
    list_display = ('member', 'quota_type', 'last_invoice_date', 'needs_invoice')
    list_filter = ('member', 'quota_type')
    actions = [
        'create_quote_invoices',
    ]

    def create_quote_invoices(self, request, queryset):
        quotainvoices = queryset.create_invoices(now())
        self.message_user(request, _('Created {0} quota invoices').format(len(quotainvoices)))
    create_quote_invoices.short_description = _("Create quota invoices")

    def get_queryset(self, request):
        qs = super(QuotaAdmin, self).get_queryset(request)
        qs = qs.select_related().annotate(last_invoice_date=Max('quotainvoice__date'))
        return qs

    def needs_invoice(self, obj):
        if obj.last_invoice_date is None:
            return True
        date = now()
        if obj.quota_type.periodicity == obj.quota_type.ANUAL:
            start = make_aware(datetime.datetime(date.year, 1, 1), utc)
            return obj.last_invoice_date < start
        elif obj.quota_type.periodicity == obj.quota_type.ANUAL:
            if date.month == 12:
                year = date.year + 1
                month = 1
            else:
                year = date.year
                month = date.month + 1
            start = make_aware(datetime.datetime(year, month, 1), utc)
            return obj.last_invoice_date < start
        return False
    needs_invoice.short_description = _("Needs invoice")
    needs_invoice.boolean = True

    def last_invoice_date(self, obj):
        return obj.last_invoice_date
    last_invoice_date.short_description = _("Last invoice date")


@admin.register(models.QuotaInvoice)
class QuotaInvoiceAdmin(admin.ModelAdmin):
    list_display = ('quota', 'date')
    list_filter = ('quota__member', 'quota__quota_type', 'quota__quota_type__periodicity')
    list_select_related = ('quota__member', 'quota__quota_type')
    date_hierarchy = 'date'
