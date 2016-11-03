# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Maintainer(models.Model):
    person = models.ForeignKey('accounting.Person', verbose_name=_("person"), on_delete=models.CASCADE)
    email = models.EmailField(_('email'))

    class Meta:
        verbose_name = _("maintainer")
        verbose_name_plural = _("maintainer")

    def __str__(self):
        return self.person.name


class NodeMaintainer(models.Model):
    maintainer = models.ForeignKey(Maintainer, verbose_name=_('maintainer'), on_delete=models.CASCADE)
    node = models.ForeignKey('guifi.Node', verbose_name=_('node'), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("node maintainer")
        verbose_name_plural = _("none maintainers")


class ZoneMaintainer(models.Model):
    maintainer = models.ForeignKey(Maintainer, verbose_name=_('maintainer'), on_delete=models.CASCADE)
    zone = models.ForeignKey('guifi.Zone', verbose_name=_('zone'), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("zone maintainer")
        verbose_name_plural = _("zone maintainers")
