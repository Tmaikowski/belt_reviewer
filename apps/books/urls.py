from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^show/(?P<id>\d+)/$', views.show, name="show"),
    url(r'^edit/(?P<id>\d+)/$', views.edit, name="edit"),
    url(r'^new/$', views.new, name="new"),
    url(r'^new_review/$', views.new_review, name="new_review"),
    url(r'^process_new_book/$', views.process_new_book, name="process_new_book"),
    url(r'^delete/(?P<id>\d+)$', views.delete_review, name="delete_review")
]
