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
router.register(r"instance", InstanceAPIViewSet, basename="instance")

# URL patterns for class-based views and API endpoints
urlpatterns = [
    #########################################################################
    # Instance views (HTML)
    #########################################################################
    path("instance/", InstanceListView.as_view(), name="instance_list"),
    path(
        "instance/create", InstanceCreateView.as_view(), name="instance_create"
    ),
    path(
        "instance/delete",
        InstanceBulkDeleteView.as_view(),
        name="instance_bulkdelete",
    ),
    path(
        "instance/<str:pk>/delete",
        InstanceDeleteView.as_view(),
        name="instance_delete",
    ),
    path(
        "instance/<str:pk>/update",
        InstanceChangeView.as_view(),
        name="instance_update",
    ),
    path(
        "instance/<str:pk>/",
        InstanceDetailView.as_view(),
        name="instance_detail",
    ),
    #########################################################################
    # API endpoints
    #########################################################################
    path("api/", include(router.urls)),
]
