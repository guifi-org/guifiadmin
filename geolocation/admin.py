# -*- coding: utf-8 -*-
from django.contrib import admin

from . import models


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')


@admin.register(models.State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'country')
    list_filter = ('country',)
    prepopulated_fields = {'code': ('name',)}


@admin.register(models.City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'state')
    list_filter = ('state', 'state__country')
    prepopulated_fields = {'code': ('name',)}


@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('address', 'postal_code', 'city', 'person')
    list_filter = ('city', 'city__state', 'city__state__country')
