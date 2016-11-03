# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pyGuifiAPI import GuifiAPI, GuifiApiError
from libcnml.libcnml import CNMLParser

from .cnml import get_zone_cnml
from . import guifi_settings


def update_node_status(node, status):
    api = GuifiAPI(username=guifi_settings.GUIFIAPI_USER,
                   passwd=guifi_settings.GUIFIAPI_PASS,
                   host=guifi_settings.GUIFIAPI_HOST,
                   secure=guifi_settings.GUIFIAPI_SECURE)
    api.auth()

    try:
        api.updateNode(node.gid, status=status)
    except GuifiApiError as e:
        return False, e.reason

    cnml = CNMLParser(get_zone_cnml(node.zone.gid))
    if not cnml.loaded:
        return False, "Error loading CNML file, check libcnml logs"

    try:
        node = cnml.nodes[int(node.gid)]
    except KeyError:
        return False, "Node %(node)s not found in %(zone)s zone\n" % {
            'node': node,
            'zone': node.zone.gid,
        }

    for device in node.getDevices():
        api.updateDevice(device.id, status=status)

        for interface in device.getInterfaces():
            for link in interface.getLinks():
                api.updateLink(link.id, status=status)

        for radio in device.getRadios():
            for interface in radio.getInterfaces():
                for link in interface.getLinks():
                    api.updateLink(link.id, status=status)
    return True, "Node updated"


def update_node(node, nick=None, zone=None, status=None, latitude=None, longitude=None, antenna_elevation=None):
    api = GuifiAPI(username=guifi_settings.GUIFIAPI_USER,
                   passwd=guifi_settings.GUIFIAPI_PASS,
                   host=guifi_settings.GUIFIAPI_HOST,
                   secure=guifi_settings.GUIFIAPI_SECURE)
    api.auth()

    params = {}

    if nick is not None:
        params['nick'] = nick
    if zone is not None:
        params['zone_id'] = zone.gid
    if status is not None:
        params['status'] = status
    if latitude is not None:
        params['lat'] = latitude
    if longitude is not None:
        params['lon'] = longitude
    if antenna_elevation is not None:
        params['elevation'] = antenna_elevation

    if params:
        params['nid'] = node.gid
        try:
            api.updateNode(**params)
        except GuifiApiError as e:
            return False, e.reason
    return True, 'OK'
