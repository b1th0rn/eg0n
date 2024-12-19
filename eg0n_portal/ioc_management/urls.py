from django.urls import path, include
from . import views as ioc_views
from django.views.generic import ListView, DetailView       # useful for template rendering
from .models import Vuln

urlpatterns = [

    path('', ioc_views.home, name="Home"),

    # path('vulns', vulns_views.vulns_list, name="Vulns"),  # init test
    path('vulns', ListView.as_view(queryset = Vuln.objects.all().order_by("update_date"), template_name = "vulns_list.html"), name="Vulns"),
    
    path('vulns-details', ioc_views.vulns_details, name="Vulns Details"),
]