"""UNetLab URL Configuration for the proxmox app."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ioc_management.views import (
    InstanceAPIViewSet,
    InstanceBulkDeleteView,
    InstanceChangeView,
    InstanceCreateView,
    InstanceDeleteView,
    InstanceDetailView,
    InstanceListView,
)

# DRF router for API endpoints
router = DefaultRouter()
router.register(r"ioc_management", InstanceAPIViewSet, basename="ioc-management")

# URL patterns for class-based views and API endpoints
urlpatterns = [
    #########################################################################
    # Instance views (HTML)
    #########################################################################
    path("ioc_management/", InstanceListView.as_view(), name="ioc_management_list"),
    path(
        "ioc_management/create", InstanceCreateView.as_view(), name="ioc_management_create"
    ),
    path(
        "ioc_management/delete",
        InstanceBulkDeleteView.as_view(),
        name="ioc_management_bulkdelete",
    ),
    path(
        "ioc_management/<str:pk>/delete",
        InstanceDeleteView.as_view(),
        name="ioc_management_delete",
    ),
    path(
        "ioc_management/<str:pk>/update",
        InstanceChangeView.as_view(),
        name="ioc_management_update",
    ),
    path(
        "ioc_management/<str:pk>/",
        InstanceDetailView.as_view(),
        name="ioc_management_detail",
    ),
    #########################################################################
    # API endpoints
    #########################################################################
    path("api/", include(router.urls)),
]
