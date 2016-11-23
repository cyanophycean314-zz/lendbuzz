from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.receiver, name='receiver'),
    url(r'^caller', views.caller, name='caller'),
    url(r'^player', views.player, name='player'),
]