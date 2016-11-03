# -*- coding: utf-8 -*-
from django.contrib import admin

from . import models
from geolocation.models import Address


class AddressInline(admin.TabularInline):
    model = Address


@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'fid')
    inlines = [
        AddressInline
    ]


@admin.register(models.Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('username', 'person', 'gid')
