from django.contrib import admin

from maintainers.admin import NodeMaintainerInline, ZoneMaintainerInline

from . import models
from . import forms


@admin.register(models.Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'gid')
    readonly_fields = ('name', 'gid', 'parent_zone')
    inlines = [
        ZoneMaintainerInline,
    ]

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(ZoneAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.register(models.Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'gid', 'owner', 'zone', 'status')
    list_filter = ('owner', 'zone', 'status')
    form = forms.UpdateNodeForm
    readonly_fields = ('gid',)
    inlines = [
        NodeMaintainerInline,
    ]

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(NodeAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.register(models.Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'gid', 'node', 'mainipv4', 'status', 'device_type', 'firmware')
    list_filter = ('device_type', 'firmware', 'node__owner', 'status', 'node__zone', 'node')
    readonly_fields = ('name', 'gid', 'node', 'mainipv4', 'status', 'firmware', 'device_type')

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(DeviceAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
