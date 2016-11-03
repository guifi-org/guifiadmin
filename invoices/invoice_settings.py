# -*- coding: utf-8 -*-
from django.conf import settings

INVOICE_PREFIX = getattr(settings, 'INVOICE_PREFIX', 'INV')

INVOICE_IFZ = getattr(settings, 'INVOICE_IFZ', '00000000A')
INVOICE_ADDRESS = getattr(settings, 'INVOICE_ADDRESS', 'Sample Address 1')
INVOICE_ZIP = getattr(settings, 'INVOICE_ZIP', '00000')
INVOICE_CITY = getattr(settings, 'INVOICE_CITY', 'City')
INVOICE_STATE = getattr(settings, 'INVOICE_STATE', 'State')
INVOICE_FOOTER = getattr(settings, 'INVOICE_FOOTER', "0000-0000-00-0000000000")
