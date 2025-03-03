from django.urls import path
from . import views
from django.views.generic import ListView, DetailView       # useful for template rendering

urlpatterns = [
    path('Vulns', views.vulns, name="vulns"),
    path('Hash', views.hash, name="hash"),
    path('IpAdd', views.ipadd, name="ipadd"),
    path('ScoreBoard', views.scoreboard, name="scoreboard"),
]   