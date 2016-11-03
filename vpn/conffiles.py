# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from shutil import make_archive
from tempfile import mkdtemp

from django.template.loader import render_to_string


def tinc_gateway_conf(gateway):
    return render_to_string(
        'vpn/tinc/gateway_tinc.conf', {
            'gateway': gateway,
        }
    )


def tinc_gateway_host(gateway):
    return render_to_string(
        'vpn/tinc/hosts/gateway.txt', {
            'gateway': gateway,
        }
    )


def tinc_client_tinc_up(client):
    return render_to_string(
        'vpn/tinc/client_tinc_up.sh', {
            'client': client,
        }
    )


def tinc_client_tinc_down(client):
    return render_to_string(
        'vpn/tinc/client_tinc_down.sh', {
            'client': client,
        }
    )


def tinc_client_conf(client):
    return render_to_string(
        'vpn/tinc/client_tinc.conf', {
            'client': client,
        }
    )


def tinc_client_openwrt_tinc_config(client):
    return render_to_string(
        'vpn/openwrt/config/tinc.txt', {
            'client': client,
        }
    )


def tinc_client_openwrt_firewall_config(client):
    return render_to_string(
        'vpn/openwrt/config/firewall.txt', {
            'client': client,
        }
    )


def tinc_client_host(client):
    return render_to_string(
        'vpn/tinc/hosts/client.txt', {
            'client': client,
        }
    )


def tinc_client_openwrt_config_tar(client):
    basedir = mkdtemp()
    tinc_config_base = os.path.join(basedir, 'etc', 'tinc', client.gateway.nickname)
    os.makedirs(tinc_config_base)
    os.makedirs(os.path.join(tinc_config_base, 'hosts'))

    with open(os.path.join(tinc_config_base, 'tinc.conf'), 'w') as conffile:
        conffile.write(tinc_client_conf(client))

    with open(os.path.join(tinc_config_base, 'tinc_up'), 'w') as conffile:
        conffile.write(tinc_client_tinc_up(client))

    with open(os.path.join(tinc_config_base, 'tinc_down'), 'w') as conffile:
        conffile.write(tinc_client_tinc_down(client))

    with open(os.path.join(tinc_config_base, 'hosts', client.gateway.nickname), 'w') as conffile:
        conffile.write(tinc_gateway_host(client.gateway))

    with open(os.path.join(tinc_config_base, 'hosts', client.member.username), 'w') as conffile:
        conffile.write(tinc_client_host(client))

    openwrt_config_base = os.path.join(basedir, 'etc', 'config')
    os.makedirs(openwrt_config_base)

    with open(os.path.join(openwrt_config_base, 'firewall'), 'w') as conffile:
        conffile.write(tinc_client_openwrt_firewall_config(client))

    with open(os.path.join(openwrt_config_base, 'tinc'), 'w') as conffile:
        conffile.write(tinc_client_openwrt_tinc_config(client))

    tarfile = make_archive('openwrt_config', 'gztar', root_dir=basedir)
    with open(tarfile, 'rb') as tarfile:
        return tarfile.read()
