from django.conf.urls import url

from . import views

node_id = r'(?P<gid>\d*)/'


urlpatterns = [
    url(r'^' + node_id + r'/update_status/$', views.UpdateNode.as_view(), name='guifi_update_node_status'),
]
