# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import View, FormView

from . import models
from . import forms


class BaseView(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BaseView, self).dispatch(*args, **kwargs)


class UpdateNode(BaseView, FormView):
    template_name = 'admin/guifi/node/update_status.html'
    form_class = forms.UpdateNodeStatusForm

    @property
    def node(self):
        return get_object_or_404(models.Node, gid=self.kwargs['gid'])

    def get_context_data(self, **kwargs):
        ctx = super(UpdateNode, self).get_context_data(**kwargs)
        ctx['opts'] = models.Node._meta
        ctx['original'] = self.node
        return ctx

    def get_form_kwargs(self):
        kwargs = super(UpdateNode, self).get_form_kwargs()
        kwargs['node'] = self.node
        return kwargs

    def form_valid(self, form):
        completed, message = form.save()
        if completed:
            messages.success(self.request, message)
        else:
            messages.error(self.request, message)
        return super(UpdateNode, self).form_valid(form)

    def get_success_url(self):
        return reverse('admin:guifi_node_change', args=(self.node.pk,))
