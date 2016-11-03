from django.db.models.signals import pre_save
from django.dispatch import receiver

from . import models
from .guifiapi import update_node


@receiver(pre_save, sender=models.Node)
def send_node_chanes_to_guifi(sender, instance, **kwargs):
    if not instance.sync_with_guifinet:
        return

    prev_obj = models.Node.objects.get(pk=instance.pk)
    params = {}

    if prev_obj.name != instance.name:
        params['nick'] = instance.name
    if prev_obj.zone_id != instance.zone_id:
        params['zone'] = instance.zone
    if prev_obj.status != instance.status:
        params['status'] = instance.status
    if prev_obj.latitude != instance.latitude:
        params['latitude'] = instance.latitude
    if prev_obj.longitude != instance.longitude:
        params['longitude'] = instance.longitude
    if prev_obj.antenna_elevation != instance.antenna_elevation:
        params['antenna_elevation'] = instance.antenna_elevation
    if params:
        ok, reason = update_node(instance, **params)
        if not ok:
            raise Exception(reason)
        instance.sync_with_guifinet = False
