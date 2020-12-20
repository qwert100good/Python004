from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login/', views.log_in),
    path('register/', views.register),
    path('logout/',views.log_out)
]
