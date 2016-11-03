# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Person(models.Model):
    name = models.CharField(_("name"), max_length=100)
    fid = models.CharField(_("nif/ifz"), max_length=15)

    class Meta:
        verbose_name = _("person")
        verbose_name_plural = _("persons")

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Member(models.Model):
    person = models.OneToOneField(Person, verbose_name=_("person"), on_delete=models.CASCADE)
    username = models.CharField(_("username"), max_length=100, unique=True)
    gid = models.CharField(_("guifi id"), max_length=10, unique=True)

    class Meta:
        verbose_name = _("member")
        verbose_name_plural = _("members")

    def __str__(self):
        return self.username
