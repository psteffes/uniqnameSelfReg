from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^terms/$', views.terms, name='terms'),
    url(r'^verify/$', views.verify, name='verify'),
    url(r'^confirm/$', views.confirm, name='confirm'),
    url(r'^create/(?P<token>.*)$', views.create, name='create'),
    url(r'^reactivate/$', views.reactivate, name='reactivate'),
    url(r'^password/$', views.password, name='password'),
    url(r'^create2/$', views.create2, name='create2'),
    url(r'^confirm_email/$', views.confirm_email, name='confirm_email'),
]
