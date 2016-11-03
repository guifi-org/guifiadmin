# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from guifi import guifi_settings
from guifi.cnml import fetch_guifi_data


class Command(BaseCommand):
    help = "Fetch guifi.net zone data."

    def handle(self, *args, **kwargs):
        fetch_guifi_data(guifi_settings.ROOT_ZONE_ID)
