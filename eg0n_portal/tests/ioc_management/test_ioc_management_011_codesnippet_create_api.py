"""Test DRF (API) code snippet creation."""

import pytest
from django.urls import reverse
from rest_framework.authtoken.models import Token
from ioc_management.models import Event, CodeSnippet


@pytest.mark.django_db
@pytest.mark.parametrize("role", ["admin", "staff", "user"])
def test_ioc_management_codesnippet_create_api_user(api_client, user_set_group1, role):
    """Test DRS (API) code snippet creation."""
    user = user_set_group1[role]
    event = user.events.all().first()
    token, _ = Token.objects.get_or_create(user=user)
    headers = {"Authorization": f"Token {token}"}
    url = reverse("codesnippet-list")

    payload = {
        "code": "DIR C:\\",
        "confidence": "high",
        "description": "Code detected in internal endpoint.",
        "event": str(event.pk),
        "language": "cmd",
        "name": "Windows Code Snippet",
        "validation_status": "suspended",
    }
    
    response = api_client.post(url, payload, format="json", headers=headers)
    assert response.status_code == 201, f"Failed for user {user.username}"
    assert response.data["name"] == payload["name"], "Code Snippet not in the returning payload"
    assert (
        len(CodeSnippet.objects.filter(name=payload["name"])) == 1
    ), "Code Snippet has not been created"


@pytest.mark.django_db
def test_ioc_management_codesnippet_create_api_guest(api_client, user_set_group1):
    """Test DRS (API) code snippet creation by guest user."""
    url = reverse("vuln-list")
    event = Event.objects.all().first()
    payload = {
        "code": "DIR C:\\",
        "confidence": "high",
        "description": "Code detected in internal endpoint.",
        "event": str(event.pk),
        "language": "cmd",
        "name": "Windows Code Snippet",
        "validation_status": "suspended",
    }
    response = api_client.post(url, payload, format="json")
    assert response.status_code == 401, "Expected 401 for guest user"
    assert len(CodeSnippet.objects.filter(name=payload["name"])) == 0, "Code Snippet has been created"
