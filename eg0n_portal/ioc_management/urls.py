"""UNetLab URL Configuration for the proxmox app."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ioc_management.views import (
    EventAPIViewSet,
    EventBulkDeleteView,
    EventChangeView,
    EventCreateView,
    EventDeleteView,
    EventDetailView,
    EventListView,
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
router.register(r"event", EventAPIViewSet, basename="event")

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
    # Event views (HTML)
    #########################################################################
    path("event/", EventListView.as_view(), name="event_list"),
    path(
        "event/create", EventCreateView.as_view(), name="event_create"
    ),
    path(
        "event/delete",
        EventBulkDeleteView.as_view(),
        name="event_bulkdelete",
    ),
    path(
        "event/<str:pk>/delete",
        EventDeleteView.as_view(),
        name="event_delete",
    ),
    path(
        "event/<str:pk>/update",
        EventChangeView.as_view(),
        name="event_update",
    ),
    path(
        "event/<str:pk>/",
        EventDetailView.as_view(),
        name="event_detail",
    ),
    #########################################################################
    # API endpoints
    #########################################################################
    path("api/", include(router.urls)),
]
