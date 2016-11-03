# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from . import models


def ansible_inventory(data):
    for device in models.Device.objects.select_related('node__zone__parent_zone').all():
        if device.node.zone.parent_zone:
            if device.node.zone.parent_zone.name not in data:
                data[device.node.zone.parent_zone.name] = {
                    'children': set(),
                }
            data[device.node.zone.parent_zone.name]['children'].add(device.node.zone.name)

        if device.node.zone.name not in data:
            data[device.node.zone.name] = {
                'children': set(),
            }
        data[device.node.zone.name]['children'].add(device.node.name)

        if device.node.name not in data:
            data[device.node.name] = {
                'hosts': set(),
            }
        data[device.node.name]['hosts'].add(device.name)

    return data
