from django.conf.urls import url

from . import views

estimate = r'(?P<estimate_pk>\d*)/'
invoice = r'(?P<invoice>\d*)/'


urlpatterns = [
    url(r'^estimates/$', views.EstimateList.as_view(), name='estimate_list'),
    url(r'^estimates/' + estimate + r'$', views.EstimateDetail.as_view(), name='estimate_detail'),
    url(r'^estimates/' + estimate + r'to_invoice/$', views.EstimateToInvoice.as_view(), name='estimate_to_invoice'),
    url(r'^$', views.InvoiceList.as_view(), name='invoice_list'),
    url(r'^' + invoice + r'$', views.InvoiceDetail.as_view(), name='invoice_detail'),
]
