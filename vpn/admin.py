# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from . import models


@admin.register(models.TincGateway)
class TincGatewayAdmin(admin.ModelAdmin):
    list_display = ('title', 'nickname', 'address', 'device', 'inet_interface', 'inet_address', 'upload', 'download', 'used_download')
    list_filter = ('device__node__zone',)
    fieldsets = (
        (None, {
            'fields': ('title', ('device', 'address', 'upload', 'download')),
        }),
        ('tinc', {
            'fields': ('nickname', ('vpn_address', 'subnet'), 'public_key', 'private_key'),
        }),
        ('shorewall', {
            'fields': (('inet_zone', 'inet_interface'), 'inet_address'),
        }),
    )

    def used_download(self, obj):
        return '<div style="width: 100%; border:1px solid black;" title="{percent}%"><div style="width: {percent}%; background-color: green;">&nbsp;</div></div>'.format(percent=obj.used_download_percent)
    used_download.short_description = _('Download %')
    used_download.allow_tags = True


@admin.register(models.TincClient)
class TincClientAdmin(admin.ModelAdmin):
    list_display = ('member', 'gateway', 'vpn_address', 'upload', 'download')
    list_filter = ('gateway',)
    fieldsets = (
        (None, {
            'fields': (('member', 'gateway'), ('upload', 'download')),
        }),
        ('tinc', {
            'fields': ('vpn_address', 'private_key', 'public_key'),
        })
    )
