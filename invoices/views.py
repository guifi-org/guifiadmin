# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import View, ListView, DetailView

from . import models


class BaseView(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BaseView, self).dispatch(*args, **kwargs)


class BaseEstimateView(BaseView):
    model = models.Estimate
    pk_url_kwarg = 'estimate_pk'


class EstimateList(BaseEstimateView, ListView):
    def get_queryset(self):
        qs = super(EstimateList, self).get_queryset()
        if 'numbers' in self.request.GET:
            qs = qs.filter(pk__in=self.request.GET['numbers'].split(','))
        return qs


class EstimateDetail(BaseEstimateView, DetailView):
    pass


class EstimateToInvoice(BaseEstimateView, DetailView):
    def get(self, request, *args, **kwargs):
        estimate = self.get_object()
        invoice = estimate.convert_to_invoice()
        return HttpResponseRedirect(invoice.get_absolute_url())


class BaseInvoiceView(BaseView):
    model = models.Invoice
    slug_field = 'number'
    slug_url_kwarg = 'invoice'

    def get_context_data(self, **kwargs):
        ctx = super(BaseInvoiceView, self).get_context_data(**kwargs)
        ctx.update({
            'invoice_ifz': settings.INVOICE_IFZ,
            'invoice_address': settings.INVOICE_ADDRESS,
            'invoice_zip': settings.INVOICE_ZIP,
            'invoice_city': settings.INVOICE_CITY,
            'invoice_state': settings.INVOICE_STATE,
            'invoice_footer': settings.INVOICE_FOOTER,
        })
        return ctx


class InvoiceList(BaseInvoiceView, ListView):
    def get_queryset(self):
        qs = super(InvoiceList, self).get_queryset()
        if 'numbers' in self.request.GET:
            qs = qs.filter(number__in=self.request.GET['numbers'].split(','))
        return qs


class InvoiceDetail(BaseInvoiceView, DetailView):
    pass
