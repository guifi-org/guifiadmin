# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Country(models.Model):
    name = models.CharField(_("name"), max_length=50)
    code = models.SlugField(_("code"), max_length=10, unique=True)

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")

    def __str__(self):
        return self.code


@python_2_unicode_compatible
class State(models.Model):
    country = models.ForeignKey(Country, verbose_name=_("country"), on_delete=models.CASCADE)
    name = models.CharField(_("name"), max_length=50)
    code = models.SlugField(_("code"), max_length=50, unique=True)

    class Meta:
        verbose_name = _("state")
        verbose_name_plural = _("states")

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class City(models.Model):
    state = models.ForeignKey(State, verbose_name=_("state"), on_delete=models.CASCADE)
    name = models.CharField(_("name"), max_length=50)
    code = models.SlugField(_("code"), max_length=50, unique=True)

    class Meta:
        verbose_name = _("city")
        verbose_name_plural = _("cities")

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Address(models.Model):
    city = models.ForeignKey(City, verbose_name=_("city"), on_delete=models.CASCADE)
    address = models.CharField(_("address"), max_length=100)
    postal_code = models.CharField(_("postal code"), max_length=10)
    person = models.ForeignKey('accounting.Person', verbose_name=_("person"), blank=True, null=True, related_name='+', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("address")
        verbose_name_plural = _("addresses")

    def __str__(self):
        return "{} {} {} {}".format(self.address, self.postal_code, self.city.name, self.city.state.name)
