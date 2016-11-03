# -*- coding: utf-8 -*-
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _

from . import models
from . import forms


class EstimateLineInline(admin.TabularInline):
    model = models.EstimateLine
    form = forms.EstimateLineForm
    readonly_fields = ('total',)


class InvoiceLineInline(admin.TabularInline):
    model = models.InvoiceLine
    form = forms.InvoiceLineForm
    readonly_fields = ('total',)


@admin.register(models.VAT)
class VATAdmin(admin.ModelAdmin):
    list_display = ('percent',)


@admin.register(models.Estimate)
class EstimateAdmin(admin.ModelAdmin):
    list_display = ('date', 'person', 'total')
    list_filter = ('person',)
    date_hierarchy = 'date'
    form = forms.InvoiceForm
    readonly_fields = ('total',)
    inlines = (
        EstimateLineInline,
    )
    actions = [
        'show_estimates',
        'convert_to_invoice',
    ]

    def show_estimates(self, request, queryset):
        pks = ",".join(str(i) for i in queryset.values_list('pk', flat=True))
        url = '{url}?numbers={numbers}'.format(
            url=reverse('estimate_list'),
            numbers=pks,
        )
        return HttpResponseRedirect(url)
    show_estimates.short_description = _("show estimates")

    def convert_to_invoice(self, request, queryset):
        for estimate in queryset:
            estimate.convert_to_invoice()
        return HttpResponseRedirect(reverse('admin:invoices_invoice_changelist'))


@admin.register(models.Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'date', 'person', 'total', 'estimate', 'is_paid')
    list_filter = ('is_paid', 'person',)
    date_hierarchy = 'date'
    form = forms.InvoiceForm
    readonly_fields = ('total', 'invoice_number')
    inlines = (
        InvoiceLineInline,
    )
    actions = [
        'show_invoices',
        'mark_as_paid',
    ]

    def show_invoices(self, request, queryset):
        numbers = ",".join(str(i) for i in queryset.values_list('number', flat=True))
        url = '{url}?numbers={numbers}'.format(
            url=reverse('invoice_list'),
            numbers=numbers,
        )
        return HttpResponseRedirect(url)
    show_invoices.short_description = _("show invoices")

    def mark_as_paid(self, request, queryset):
        for invoice in queryset:
            invoice.is_paid = True
            invoice.save()
        return HttpResponseRedirect(reverse('admin:invoices_invoice_changelist'))
    mark_as_paid.short_description = _("mark as paid")
