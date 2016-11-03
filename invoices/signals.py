from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from . import models


@receiver(post_save, sender=models.InvoiceLine)
def update_invoice_total_on_line_change(sender, instance, *args, **kwargs):
    instance.invoice.update_total()
    instance.invoice.save()


@receiver(post_delete, sender=models.InvoiceLine)
def update_invoice_total_on_line_deletion(sender, instance, *args, **kwargs):
    instance.invoice.update_total()
    instance.invoice.save()
