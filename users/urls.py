# users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # path('signup/', views.SignUp.as_view(), name='signup'),
    # path('login/', views.SignUp.as_view(), name='login'),
    path('signup/', views.SignUp, name='signup'),
    path('login/', views.login, name='login'),

]
