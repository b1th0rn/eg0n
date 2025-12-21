"""URL configuration for IoC Management app."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ioc_management.views import (
    CodeSnippetAPIViewSet,
    EventAPIViewSet,
    EventBulkDeleteView,
    EventChangeView,
    EventCreateView,
    EventDeleteView,
    EventDetailView,
    EventListView,
    FQDNAPIViewSet,
    HashAPIViewSet,
    IpAddAPIViewSet,
    VulnAPIViewSet,
)

# DRF router for API endpoints
router = DefaultRouter()
router.register(r"codesnippet", CodeSnippetAPIViewSet, basename="codesnippet")
router.register(r"event", EventAPIViewSet, basename="event")
router.register(r"fqdn", FQDNAPIViewSet, basename="fqdn")
router.register(r"hash", HashAPIViewSet, basename="hash")
router.register(r"ipadd", IpAddAPIViewSet, basename="ipadd")
router.register(r"vuln", VulnAPIViewSet, basename="vuln")

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
