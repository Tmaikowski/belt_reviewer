from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^show/(?P<id>\d+)$', views.show, name="show"),
    url(r'^process_registration$', views.process_registration, name="process_registration"),
    url(r'^process_login$', views.process_login, name="process_login"),
    url(r'^logout/$', views.logout, name="logout")
]
