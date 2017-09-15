from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^secure/activation_link/$', views.activation_link),
    url(r'^get_suggestions/$', views.get_suggestions),
    url(r'^find_uniqname/$', views.find_uniqname),
    url(r'^validate_password/$', views.validate_password),
]
