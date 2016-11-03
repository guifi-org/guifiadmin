# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from . import guifi_settings


@python_2_unicode_compatible
class Zone(models.Model):
    name = models.CharField(_("name"), max_length=100, unique=True)
    gid = models.CharField(_("guifi id"), max_length=10, unique=True)
    parent_zone = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("zone")
        verbose_name_plural = _("zones")
        ordering = ('name', )

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Node(models.Model):
    name = models.CharField(_("name"), max_length=100)
    # description = models.TextField(_("description"), blank=True, null=True)  # TODO: add this param to libcnml
    gid = models.CharField(_("guifi id"), max_length=10, unique=True)
    owner = models.ForeignKey("accounting.Member", verbose_name=_("owner"), blank=True, null=True, on_delete=models.SET_NULL)
    zone = models.ForeignKey(Zone, verbose_name=_("zone"), on_delete=models.CASCADE)
    status = models.CharField(_("status"), max_length=30, choices=((x, x) for x in guifi_settings.STATUSES))
    latitude = models.CharField(_("latitude"), max_length=50)
    longitude = models.CharField(_("longitude"), max_length=50)
    antenna_elevation = models.IntegerField(_("antenna elevation"))
    # graph_server = models.CharField(_("Graph server"), max_length=50, blank=True, null=True)  # TODO: add this param to libcnml

    sync_with_guifinet = models.BooleanField(_("Sync with guifi.net"), default=False, help_text=_("When this checkbox is active changes will be commited to guifi.net."))

    @property
    def guifi_url(self):
        return guifi_settings.NODE_URL.format(nodeid=self.gid)

    class Meta:
        verbose_name = _("node")
        verbose_name_plural = _("nodes")
        ordering = ('name', )

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Device(models.Model):
    name = models.CharField(_("name"), max_length=100)
    gid = models.CharField(_("guifi id"), max_length=10, unique=True)
    node = models.ForeignKey(Node, verbose_name=_("node"), on_delete=models.CASCADE)
    mainipv4 = models.CharField(_("main IPv4"), max_length=20)
    status = models.CharField(_("status"), max_length=30, choices=((x, x) for x in guifi_settings.STATUSES))
    firmware = models.CharField(_("firmware"), max_length=100)
    device_type = models.CharField(_("type"), max_length=50)

    class Meta:
        verbose_name = _("device")
        verbose_name_plural = _("device")
        ordering = ('name', )

    def __str__(self):
        return self.name
