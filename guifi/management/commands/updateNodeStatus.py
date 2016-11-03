# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand, CommandError

from guifi import guifi_settings
from guifi.guifi_settings import STATUSES
from guifi.guifiapi import update_node
from guifi.models import Node


class Command(BaseCommand):
    help = "Recursively update a node status."

    def add_arguments(self, parser):
        parser.add_argument('-u', '--user', type=str, help="guifi.net username, by default GUIFIAPI_USER setting.", default=None)
        parser.add_argument('-p', '--passwd', type=str, help="guifi.net password, by default GUIFIAPI_PASS setting.", default=None)
        parser.add_argument('--host', type=str, help="guifi.net server", default=guifi_settings.GUIFIAPI_HOST)
        parser.add_argument('-n', '--nodeid', type=str, required=True, help="guifi.net password, by default GUIFIAPI_PASS setting.")
        parser.add_argument('-s', '--status', type=str, required=True, choices=STATUSES, help="target status", default="Working")

    def handle(self, *args, **options):
        node = Node.objects.filter(gid=options['nodeid']).first()
        if node is None:
            raise CommandError("Node {} not found.".format(options['nodeid']))
        success, message = update_node(
            node=node,
            status=options['status'],
            username=options.get('user') or guifi_settings.GUIFIAPI_USER,
            passwd=options.get('passwd') or guifi_settings.GUIFIAPI_PASS,
            host=options['host'],
        )
        if success:
            self.stdout.write(message)
        else:
            raise CommandError(message)
