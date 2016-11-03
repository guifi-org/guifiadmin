# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.core.management import BaseCommand
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now, make_aware, utc

from quotas import models

DATE_FORMAT = "%Y-%m-%d"


class Command(BaseCommand):
    help_text = _("Create invoices for quotas.")

    def add_arguments(self, parser):
        parser.add_argument('-d', '--date', metavar="YYYY-MM-DD", help=_('Create quotas for the month of the given date.'))

    def handle(self, *args, **options):
        date = options['date']
        if date is None:
            date = now()
        else:
            date = make_aware(
                datetime.datetime.strptime(date, DATE_FORMAT),
                utc,
            )

        print date
        models.Quota.objects.create_invoices(date)
