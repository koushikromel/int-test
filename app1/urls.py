from django.urls import path
from . import views


urlpatterns = [
    path("", views.index),
    path("metar/ping", views.ping),
    path("metar/info", views.info),
]