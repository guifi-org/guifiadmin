# -*- coding: utf-8 -*-
from django import forms

from . import models


class EstimateLineForm(forms.ModelForm):
    class Meta:
        model = models.EstimateLine
        exclude = (
            'total',
        )


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = models.Invoice
        exclude = (
            'number',
            'total',
        )


class InvoiceLineForm(forms.ModelForm):
    class Meta:
        model = models.InvoiceLine
        exclude = (
            'total',
        )
