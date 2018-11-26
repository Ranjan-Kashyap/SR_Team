# users/urls.py
from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('signup/', views.SignUp, name='signup'),
    path('login/', views.login, name='login'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]
