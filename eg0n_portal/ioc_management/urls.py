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
)

# DRF router for API endpoints
router = DefaultRouter()
router.register(r"event", EventAPIViewSet, basename="event")

# URL patterns for class-based views and API endpoints
urlpatterns = [
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
