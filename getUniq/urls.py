from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^terms/$', views.terms, name='terms'),
    url(r'^verify/$', views.verify, name='verify'),
    url(r'^confirm_email/$', views.confirm_email, name='confirm_email'),
    url(r'^create/(?P<token>.*)$', views.create, name='create'),
    url(r'^reactivate/$', views.reactivate, name='reactivate'),
    url(r'^password/$', views.password, name='password'),
    url(r'^success/$', views.success, name='success'),
    url(r'^test_create/$', views.test_create, name='test_create'),
    url(r'^test_password/$', views.test_password, name='test_password'),
]
