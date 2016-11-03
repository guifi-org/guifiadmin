# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from . import models


def ansible_inventory(data):
    if 'gateways' not in data:
        data['gateways'] = {
            'hosts': [],
        }

    for gateway in models.TincGateway.objects.all():
        if gateway.address not in data['gateways']['hosts']:
            data['gateways']['hosts'].append(gateway.address)
        serverdata = data['_meta']['hostvars'].get(gateway.address, {
            'ansible_user': 'root',
            'vpns': [],
        })
        serverdata['vpns'].append({
            'address': gateway.get_address(),
            'nickname': gateway.nickname,
            'inet_zone': gateway.inet_zone,
            'inet_interface': gateway.inet_interface,
            'inet_address': gateway.inet_address,
            'vpn_address': gateway.vpn_address,
            'subnet': gateway.subnet,
            'private_key': gateway.private_key,
            'public_key': gateway.public_key,
        })
        data['_meta']['hostvars'][gateway.address] = serverdata
    return data
