from django.urls import path, include
from . import views as ioc_views
from django.views.generic import ListView, DetailView       # useful for template rendering

urlpatterns = [

    # Home page
    path('', ioc_views.home, name='Home'),
    # IP list
    path('ip_list/', ioc_views.ip_list, name='IP Address List'),
    # Domain list
    path('domain_list/', ioc_views.domain_list, name='DomainName List'),

]