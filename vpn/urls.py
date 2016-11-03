# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from . import views

client = r'(?P<pk>\d*)/'
gateway = r'(?P<pk>\d*)/'

urlpatterns = [
    url(r'^gateway/' + gateway + r'tinc.conf$', views.TincGatewayConfView.as_view(), name='vpn_tinc_gateway_conf'),
    url(r'^gateway/' + gateway + r'host$', views.TincGatewayHostView.as_view(), name='vpn_tinc_gateway_host'),
    url(r'^client/' + client + r'tinc.conf$', views.TincClientConfView.as_view(), name='vpn_tinc_client_conf'),
    url(r'^client/' + client + r'tinc_up$', views.TincClientTincUp.as_view(), name='vpn_tinc_client_tinc_up'),
    url(r'^client/' + client + r'tinc_down$', views.TincClientTincDown.as_view(), name='vpn_tinc_client_tinc_down'),
    url(r'^client/' + client + r'host$', views.TincClientHostView.as_view(), name='vpn_tinc_client_host'),
    url(r'^client/' + client + r'openwrt.tinc.config$', views.TincClientOpenWRTTincConfig.as_view(), name='vpn_tinc_client_openwrt_tinc_config'),
    url(r'^client/' + client + r'openwrt.firewall.config$', views.TincClientOpenWRTFirewallConfig.as_view(), name='vpn_tinc_client_openwrt_firewall_config'),
    url(r'^client/' + client + r'openwrt.tar.gz$', views.TincClientOpenWRTTarGz.as_view(), name='vpn_tinc_client_openwrt_tar_gz'),
]
