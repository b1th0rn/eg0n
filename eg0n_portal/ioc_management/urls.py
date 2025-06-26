from django.urls import path
from . import views

urlpatterns = [
    path('Vulns', views.vulns, name="vulns"),
    path('Hash', views.hash, name="hash"),
    path('IpAdd', views.ipadd, name="ipadd"),
    path('ScoreBoard', views.scoreboard, name="scoreboard"),
]   