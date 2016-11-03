# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin

from . import models
from . import conffiles


class BaseView(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BaseView, self).dispatch(*args, **kwargs)


class BaseConfigView(BaseView, SingleObjectMixin):
    content_type = 'text/plain'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        conffile = self.get_configuration()
        return HttpResponse(conffile, content_type=self.content_type)

    def get_configuration(self):
        raise NotImplementedError()


class TincGatewayConfView(BaseConfigView):
    model = models.TincGateway
    conffile_func = conffiles.tinc_gateway_conf

    def get_configuration(self):
        return conffiles.tinc_gateway_conf(self.object)


class TincClientConfView(BaseConfigView):
    model = models.TincClient

    def get_configuration(self):
        return conffiles.tinc_client_conf(self.object)


class TincClientTincUp(BaseConfigView):
    model = models.TincClient

    def get_configuration(self):
        return conffiles.tinc_client_tinc_up(self.object)


class TincClientTincDown(BaseConfigView):
    model = models.TincClient

    def get_configuration(self):
        return conffiles.tinc_client_tinc_down(self.object)


class TincGatewayHostView(BaseConfigView):
    model = models.TincGateway

    def get_configuration(self):
        return conffiles.tinc_gateway_host(self.object)


class TincClientHostView(BaseConfigView):
    model = models.TincClient

    def get_configuration(self):
        return conffiles.tinc_client_host(self.object)


class TincClientOpenWRTTincConfig(BaseConfigView):
    model = models.TincClient

    def get_configuration(self):
        return conffiles.tinc_client_openwrt_tinc_config(self.object)


class TincClientOpenWRTFirewallConfig(BaseConfigView):
    model = models.TincClient

    def get_configuration(self):
        return conffiles.tinc_client_openwrt_firewall_config(self.object)


class TincClientOpenWRTTarGz(BaseConfigView):
    content_type = 'application/x-gtar-compressed'
    model = models.TincClient

    def get_configuration(self):
        return conffiles.tinc_client_openwrt_config_tar(self.object)
