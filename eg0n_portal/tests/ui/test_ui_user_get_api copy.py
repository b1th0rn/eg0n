# """Test API authentication."""

# from django.urls import reverse
# from rest_framework.authtoken.models import Token

# def test_ui_authentication_api_admin(api_client, user_set):
#     """Test API authentication by admin."""
#     token, _ = Token.objects.get_or_create(user=user_set[0]["admin"])
#     headers = {"Authorization": f"Token {token}"}
#     url = reverse("user-list")
#     response = api_client.get(url, headers=headers)
#     assert response.status_code == 200
#     assert any(user['username'] == "admin1" for user in response.data["results"])
#     assert any(user['username'] == "staff1" for user in response.data["results"])
#     assert any(user['username'] == "user1" for user in response.data["results"])
#     assert any(user['username'] == "admin2" for user in response.data["results"])
#     assert any(user['username'] == "staff2" for user in response.data["results"])
#     assert any(user['username'] == "user2" for user in response.data["results"])
#     assert any(user['username'] == "admin3" for user in response.data["results"])
#     assert any(user['username'] == "staff3" for user in response.data["results"])
#     assert any(user['username'] == "user3" for user in response.data["results"])


# def test_ui_authentication_api_staff(api_client, user_set):
#     """Test API authentication by stagg."""
#     token, _ = Token.objects.get_or_create(user=user_set[0]["staff"])
#     headers = {"Authorization": f"Token {token}"}
#     url = reverse("user-list")
#     response = api_client.get(url, headers=headers)
#     assert response.status_code == 200
#     assert any(user['username'] == "admin1" for user in response.data["results"])
#     assert any(user['username'] == "staff1" for user in response.data["results"])
#     assert any(user['username'] == "user1" for user in response.data["results"])
#     assert not any(user['username'] == "admin2" for user in response.data["results"])
#     assert not any(user['username'] == "staff2" for user in response.data["results"])
#     assert not any(user['username'] == "user2" for user in response.data["results"])
#     assert not any(user['username'] == "admin3" for user in response.data["results"])
#     assert not any(user['username'] == "staff3" for user in response.data["results"])
#     assert not any(user['username'] == "user3" for user in response.data["results"])



# # def test_ui_authentication_token_api_guest(api_client, user_group):
# #     """Test UI token creation by non-existent user."""
# #     url = reverse("api_token")
# #     data = {"username": "guest", "password": "guest_pass"}
# #     response = api_client.post(url, data, format="json")
# #     assert response.status_code == 400

# # def test_ui_authentication_api_token_staff(api_client, staff_user):
# #     """Test API authentication by staff."""
# #     url = reverse("api_user")
# #     data = {"username": "staff", "password": "staff1_pass"}
# #     response = api_client.post(url, data, format="json")
# #     assert response.status_code == 200
# #     assert "token" in response.data
# #     assert len(response.data["token"]) > 0


# # def test_ui_authentication_api_token_user(api_client, user):
# #     """Test API authentication by user."""
# #     url = reverse("api_user")
# #     data = {"username": "user", "password": "user1_pass"}
# #     response = api_client.post(url, data, format="json")
# #     assert response.status_code == 200
# #     assert "token" in response.data
# #     assert len(response.data["token"]) > 0


# # def test_ui_authentication_api_token_guest(api_client, db):
# #     """Test UI authentication by non-existent user."""
# #     url = reverse("api_user")
# #     data = {"username": "guest", "password": "guest_pass"}
# #     response = api_client.post(url, data, format="json")
# #     assert response.status_code == 400
