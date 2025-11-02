"""Test HTML (UI) profile view."""

from bs4 import BeautifulSoup
import pytest
from django.urls import reverse


@pytest.mark.parametrize("role", ["admin", "staff", "user"])
def test_ui_profile_update_html_user(client, user_set_group1, role):
    """Test HTML (UI) user profile update."""
    user = user_set_group1[role]
    client.force_login(user)
    url = reverse("user_update", kwargs={"pk": user.id})
    payload = {"first_name": f"New {user.username} Name"}
    response = client.post(url, payload, format="json")
    assert (
        response.status_code == 200
    ), f"Expected 200 for user {user.username} ({role})"
    # Verify the change
    url = reverse("user_detail", kwargs={"pk": user.id})
    response = client.get(url)
    assert response.status_code == 200, (
        f"Expected 200 for user {user.username} ({role})" + response.text
    )
    html = response.content.decode()
    soup = BeautifulSoup(html, "html.parser")
    card_bodies = soup.find_all("div", class_="card-body")
    assert any(
        user.first_name in div.get_text(strip=True) for div in card_bodies
    ), f"First name not found for user {user.username} ({role})"
