#!/usr/bin/env python
import os
import argparse
import django

from guifiadmin.extended_json import dumps

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "guifiadmin.settings")
django.setup()


parser = argparse.ArgumentParser(
    description="Ansible inventory"
)
parser.add_argument('--list', action='store_true', help='return full ansible inventory.')

if __name__ == "__main__":

    from guifi.inventory import ansible_inventory as guifi_inventory
    from vpn.inventory import ansible_inventory as vpn_inventory
    args = parser.parse_args()
    if args.list:
        data = {
            '_meta': {
                'hostvars': {}
            },
        }
        data = guifi_inventory(data)
        data = vpn_inventory(data)
    else:
        data = '{}'  # No response for other parametters
    print dumps(data, indent=4)
