from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('registration', views.register),
    path('success', views.login),
    path('dashboard', views.success),
    path('logout', views.logout),

]
