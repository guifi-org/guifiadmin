# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from . import utils


@python_2_unicode_compatible
class TincGateway(models.Model):
    title = models.CharField(_("title"), max_length=200)
    nickname = models.SlugField(_("nickname"), max_length=100, unique=True, help_text=_("name of the tinc daemon and the network interface"))
    address = models.CharField(_("address"), max_length=200, blank=True, null=True, help_text=_("IP address or hostname of the server. If blank, guifi address will be used."))
    device = models.ForeignKey('guifi.Device', verbose_name=_("device"), on_delete=models.CASCADE)
    upload = models.PositiveSmallIntegerField(_("upload"), help_text=_('speed in kbit/s'))
    download = models.PositiveSmallIntegerField(_("download"), help_text=_('speed in kbit/s'))
    inet_zone = models.CharField(_("external zone"), max_length=20, default="inet", help_text=_("zone for the external interface."))
    inet_interface = models.CharField(_("external interface"), max_length=20, help_text=_("external interface. For firewall policies."))
    inet_address = models.CharField(_("external address"), max_length=200, help_text=_("external ip address. VPN traffic will go out from here."))
    vpn_address = models.CharField(_("vpn address"), max_length=200)
    subnet = models.CharField(_("subnet"), max_length=200)
    private_key = models.TextField(_("private key"), blank=True, null=True)
    public_key = models.TextField(_("public key"), blank=True, null=True)

    class Meta:
        verbose_name = _("Tinc server")
        verbose_name_plural = _("Tinc servers")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.private_key:
            self.private_key, self.public_key = utils.generate_RSA()
        super(TincGateway, self).save(*args, **kwargs)

    @property
    def used_download_percent(self):
        total = self.tincclient_set.aggregate(total=models.Sum('download'))['total']
        if total is None:
            return 0
        return total * 100 / self.download

    def get_address(self):
        return self.address or self.device.mainipv4


class TincClient(models.Model):
    member = models.ForeignKey('accounting.Member', verbose_name=_("member"), on_delete=models.CASCADE)
    gateway = models.ForeignKey(TincGateway, verbose_name=_("gateway"), on_delete=models.CASCADE)
    vpn_address = models.CharField(_("vpn address"), max_length=200)
    private_key = models.TextField(_("private key"), blank=True, null=True)
    public_key = models.TextField(_("public key"), blank=True, null=True)
    upload = models.PositiveSmallIntegerField(_("upload"), help_text=_('speed in kbit/s'), default=400)
    download = models.PositiveSmallIntegerField(_("download"), help_text=_('speed in kbit/s'), default=4000)

    class Meta:
        verbose_name = _("Tinc client")
        verbose_name_plural = _("Tinc clients")

    def __str__(self):
        return "{}:{}".format(self.gateway.title, self.member.person.name)

    def save(self, *args, **kwargs):
        if not self.private_key:
            self.private_key, self.public_key = utils.generate_RSA()
        super(TincClient, self).save(*args, **kwargs)
