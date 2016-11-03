# -*- coding: utf-8 -*-
import os
from django.conf import settings

CNML_FOLDER = getattr(settings, 'CNML_FOLDER', os.path.join(
    settings.BASE_DIR, '.cache', 'cnml'
))

CACHE_DURATION = getattr(settings, 'CACHE_DURATION', 24 * 60 * 60)

CNML_URL = getattr(settings, "CNML_URL", "https://guifi.net/eu/guifi/cnml/{zoneid}/detail")
NODE_URL = getattr(settings, "NODE_URL", "https://guifi.net/eu/node/{nodeid}")

# https://guifi.net/en/guifi/cnml/17718/detail
ROOT_ZONE_ID = getattr(settings, "ROOT_ZONE_ID", 17718)

GUIFIAPI_USER = getattr(settings, 'GUIFIAPI_USER', None)
GUIFIAPI_PASS = getattr(settings, 'GUIFIAPI_PASS', None)
GUIFIAPI_HOST = getattr(settings, 'GUIFIAPI_HOST', 'guifi.net')
GUIFIAPI_SECURE = getattr(settings, 'GUIFIAPI_SECURE', True)


STATUSES = ['Planned', 'Working', 'Testing', 'Building', 'Reserved', 'Dropped']
