from django.urls import path, include
from . import views as ioc_views
from django.views.generic import ListView, DetailView # useful for template rendering
from ioc_management.models import IpAdd

urlpatterns = [

    # Home page
    # path('', ioc_views.home, name='Home'),

    # IP list
    # path('ip_list/', ioc_views.ip_list, name='IP Address List'),
    path('ip_list/', ListView.as_view(
        queryset = IpAdd.objects.all().order_by('-created_at'),
        template_name = 'ip_list.html'), name='IP Address List'),

    # Domain list
    path('domain_list/', ioc_views.domain_list, name='DomainName List'),

]