from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^quotes$', views.quotes),
    url(r'^add$', views.add),  
    url(r'^favourite/(?P<number>\d+)$', views.favourite),
    url(r'^users/(?P<number>\d+)$', views.users),
    url(r'^remove/(?P<number>\d+)$', views.remove),
    url(r'^logout$', views.logout)
]