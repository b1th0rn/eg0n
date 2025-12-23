"""Test DRF (API) FQDN creation."""

import pytest
from django.urls import reverse
from rest_framework.authtoken.models import Token
from ioc_management.models import Event, FQDN


@pytest.mark.django_db
@pytest.mark.parametrize("role", ["admin", "staff", "user"])
def test_ioc_management_fqdn_create_api_user(api_client, user_set_group1, role):
    """Test DRS (API) FQDN creation."""
    user = user_set_group1[role]
    event = user.events.all().first()
    token, _ = Token.objects.get_or_create(user=user)
    headers = {"Authorization": f"Token {token}"}
    url = reverse("fqdn-list")

    payload = {
        "confidence": "high",
        "description": "FQDN detected in phishing email.",
        "event": str(event.pk),
        "fqdn": "www-123.example-123.com",
        "validation_status": "suspended",
    }
    
    response = api_client.post(url, payload, format="json", headers=headers)
    assert response.status_code == 201, f"Failed for user {user.username}"
    assert response.data["fqdn"] == payload["fqdn"], "FQDN not in the returning payload"
    qs = FQDN.objects.filter(fqdn=payload["fqdn"])
    assert (len(qs) == 1), "FQDN has not been created"
    assert qs.first().author == user, "Author is not set"


@pytest.mark.django_db
def test_ioc_management_fqdn_create_api_guest(api_client, user_set_group1):
    """Test DRS (API) FQDN creation by guest user."""
    url = reverse("vuln-list")
    event = Event.objects.all().first()
    payload = {
        "confidence": "high",
        "description": "FQDN detected in phishing email.",
        "event": str(event.pk),
        "fqdn": "www-123.example-123.com",
        "validation_status": "suspended",
    }
    response = api_client.post(url, payload, format="json")
    assert response.status_code == 401, "Expected 401 for guest user"
    assert len(FQDN.objects.filter(fqdn=payload["fqdn"])) == 0, "FQDN has been created"
