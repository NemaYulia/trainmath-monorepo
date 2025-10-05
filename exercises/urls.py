# exercises/urls.py
from django.urls import path
from . import views

app_name = 'exercises'

urlpatterns = [
    path("", views.exercises_home, name="exercises_home"),
    path("stats/", views.stats_view, name="stats"),
]
