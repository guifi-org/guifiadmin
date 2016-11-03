from django.contrib import admin

from . import models


@admin.register(models.Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'date', 'provider', 'total')
    list_filter = ('provider',)
    date_hierarchy = 'date'
