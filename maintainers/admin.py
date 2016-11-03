from django.contrib import admin

from . import models


class NodeMaintainerInline(admin.TabularInline):
    model = models.NodeMaintainer


class ZoneMaintainerInline(admin.TabularInline):
    model = models.ZoneMaintainer


@admin.register(models.Maintainer)
class MaintainerAdmin(admin.ModelAdmin):
    list_display = ('person', 'email')
    inlines = [
        NodeMaintainerInline,
        ZoneMaintainerInline,
    ]
