import pytest
import uuid
from api_client import FavQsClient

@pytest.fixture(scope="session")
def api_client():
    return FavQsClient()

@pytest.fixture
def user_data_factory():
    def _generate_data():
        unique_id = str(uuid.uuid4())[:8]
        return {
            "login": f"user_{unique_id}",
            "email": f"test_{unique_id}@example.com",
            "password": "StrongPassword123!"
        }
    return _generate_data


@pytest.fixture
def created_user(api_client, user_data_factory):
    user_info = user_data_factory()
    response = api_client.post("/users", payload={"user": user_info})
    assert response.status_code == 200, f"Error creating a user: {response.text}"

    response_json = response.json()
    user_token = response_json.get("User-Token")
    login = response_json.get("login")
    assert user_token, f"The response does not contain a User-Token: {response.text}"
    assert login, f"The response does not contain a login: {response.text}"

    return {
        "login": login,
        "user_token": user_token,
        "user_info": user_info,
    }