
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('fetchVideo', views.fetchVideo, name="fetchVideo"),
    path('fetchVaccCenter', views.temp_fetchVaccCenter_redirect,
         name="fetchVaccCenter"),

]
