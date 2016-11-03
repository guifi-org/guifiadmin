# -*- coding: utf-8 -*-
from django.conf import settings

RSA_BITS = getattr(settings, 'RSA_BITS', 4096)
