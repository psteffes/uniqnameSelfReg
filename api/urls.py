from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^secure/activation_link/$', views.activation_link, name='activation_link'),
    url(r'^get_suggestions/$', views.get_suggestions, name='get_suggestions'),
    url(r'^find_uniqname/$', views.find_uniqname, name='find_uniqname'),
    url(r'^validate_password/$', views.validate_password, name='validate_password'),
]
