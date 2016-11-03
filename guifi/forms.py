# -*- coding: utf-8 -*-
from django import forms

from . import guifi_settings
from . import models
from .guifiapi import update_node_status

STATUS_CHOICES = ((i, i) for i in guifi_settings.STATUSES)


class UpdateNodeStatusForm(forms.Form):
    status = forms.ChoiceField(choices=STATUS_CHOICES)

    def __init__(self, node=None, *args, **kwargs):
        super(UpdateNodeStatusForm, self).__init__(*args, **kwargs)
        self.node = node

    def save(self):
        return update_node_status(
            node=self.node,
            status=self.cleaned_data['status'],
        )


class UpdateNodeForm(forms.ModelForm):
    class Meta:
        model = models.Node
        fields = ('name', 'zone', 'status', 'latitude', 'longitude', 'antenna_elevation', 'sync_with_guifinet')
