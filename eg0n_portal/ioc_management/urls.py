from django.urls import path, include
from . import views
from django.views.generic import ListView, DetailView       # useful for template rendering
from .models import Vuln

urlpatterns = [

    # path('', ioc_views.home, name="Home"),
    # path('vulns', vulns_views.vulns_list, name="Vulns"),  # init test
    # path('vulns', ListView.as_view(queryset = Vuln.objects.all().order_by("update_date"), template_name = "vulns_list.html"), name="Vulns"),
    path('Vulns', views.vulns, name="vulns"),
    path('Hash', views.hash, name="hash"),
    path('IpAdd', views.ipadd, name="ipadd")
    # path('vulns-details', ioc_views.vulns_details, name="Vulns Details"),
]