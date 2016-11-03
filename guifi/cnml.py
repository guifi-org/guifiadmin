# -*- coding: utf-8 -*-
import os
import time
import urllib2

from libcnml.libcnml import CNMLParser, Status

from . import models
from . import guifi_settings


def get_zone_cnml(zoneid):
    cnml_file = os.path.join(guifi_settings.CNML_FOLDER, "{}.cnml".format(zoneid))
    if not os.path.exists(cnml_file) or \
            os.path.getmtime(cnml_file) - time.time() > guifi_settings.CACHE_DURATION:
        print "Descargando cnml"
        url = guifi_settings.CNML_URL.format(zoneid=zoneid)
        response = urllib2.urlopen(url)
        with open(cnml_file, 'w') as cnmlfile:
            cnmlfile.write(response.read())
    return cnml_file


def fetch_guifi_data(zoneid):
    cnml_file = get_zone_cnml(guifi_settings.ROOT_ZONE_ID)
    data = CNMLParser(cnml_file)
    existing = {
        'zones': [],
        'nodes': [],
        'devices': [],
    }
    if data.loaded:
        rootzone = data.getZone(data.rootzone)
        __add_zone(None, rootzone, existing)

    models.Zone.objects.exclude(pk__in=existing['zones']).delete()
    models.Node.objects.exclude(pk__in=existing['nodes']).delete()
    models.Device.objects.exclude(pk__in=existing['devices']).delete()


def __add_zone(parent, cnmlzone, existing):
    zone, new = models.Zone.objects.update_or_create(
        gid=cnmlzone.id,
        defaults={
            'name': cnmlzone.title,
            'parent_zone': parent,
        }
    )
    existing['zones'].append(zone.pk)

    for subzone in cnmlzone.getSubzones():
        __add_zone(zone, subzone, existing)

    for cnmlnode in cnmlzone.getNodes():
        __add_node(zone, cnmlnode, existing)


def __add_node(zone, cnmlnode, existing):
    node, new = models.Node.objects.update_or_create(
        gid=cnmlnode.id,
        defaults={
            'zone': zone,
            'name': cnmlnode.title,
            'status': Status.statusToStr(cnmlnode.status),
            'latitude': cnmlnode.latitude,
            'longitude': cnmlnode.longitude,
            'antenna_elevation': cnmlnode.antenna_elevation,
            'sync_with_guifinet': False,
        }
    )
    existing['nodes'].append(node.pk)
    for cnmldevice in cnmlnode.getDevices():
        __add_device(node, cnmldevice, existing)


def __add_device(node, cnmldevice, existing):
    device, new = models.Device.objects.update_or_create(
        gid=cnmldevice.id,
        defaults={
            'node': node,
            'name': cnmldevice.title,
            'mainipv4': '0.0.0.0',  # FIXME: datu hau ez dag libcnml-n
            'status': Status.statusToStr(cnmldevice.status),
            'firmware': cnmldevice.firmware,
            'device_type': cnmldevice.type,
        }
    )
    existing['devices'].append(device.pk)
