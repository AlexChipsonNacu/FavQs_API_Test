import pytest


def _parse_json_response(response):
    try:
        return response.json()
    except ValueError as exc:
        pytest.fail(f"The response is not valid JSON: {response.text}. Error: {exc}")


def _assert_error_response(response, expected_error_code, expected_message_snippet, allowed_statuses=(200, 400, 422)):
    assert response.status_code in allowed_statuses, (
        f"One of the status codes was expected {allowed_statuses}, but received {response.status_code}. "
        f"The body of the response: {response.text}"
    )
    data = _parse_json_response(response)
    assert data.get("error_code") == expected_error_code, f"Unexpected error_code: {data}"

    message = data.get("message")
    assert isinstance(message, str), f"A string field named message was expected, but the following was received: {type(message)}"
    assert expected_message_snippet in message, f" Fragment '{expected_message_snippet}' not found in '{message}'"

    return data


def test_create_and_verify_user(api_client, user_data_factory):

    user_info = user_data_factory()
    payload = {"user": user_info}


    create_response = api_client.post("/users", payload=payload)
    assert create_response.status_code == 200, f"Error creating: {create_response.text}"


    user_token = create_response.json().get("User-Token")
    login = create_response.json().get("login")
    assert user_token is not None


    get_response = api_client.get(f"/users/{login}", user_token=user_token)
    assert get_response.status_code == 200

    data = get_response.json()

    assert data["login"] == user_info["login"]
    assert data["account_details"]["email"] == user_info["email"]


def test_update_and_verify_user(api_client, user_data_factory):

    initial_data = user_data_factory()
    create_res = api_client.post("/users", payload={"user": initial_data})
    user_token = create_res.json()["User-Token"]
    old_login = create_res.json()["login"]

    new_data = user_data_factory()
    update_payload = {
        "user": {
            "login": new_data["login"],
            "email": new_data["email"]
        }
    }

    update_res = api_client.put(f"/users/{old_login}", payload=update_payload, user_token=user_token)
    assert update_res.status_code == 200

    update_response_json = update_res.json()
    assert update_response_json.get("message") == "User successfully updated."


    final_get = api_client.get(f"/users/{new_data['login']}", user_token=user_token)
    assert final_get.status_code == 200

    final_data = final_get.json()
    assert final_data["login"] == new_data["login"]
    assert final_data["account_details"]["email"] == new_data["email"]


@pytest.mark.parametrize(
    "override_data, expected_error_snippet",
    [
        ({"email": "plainaddress"}, "Email is not a valid email"),
        ({"password": "123"}, "Password is too short"),
        (
            {"login": "invalid login!"},
            "Username can only contain letters (a-z), numbers (0-9) and the underscore (_)",
        ),
    ],
)
def test_create_user_validation_errors(api_client, user_data_factory, override_data, expected_error_snippet):
    user_info = user_data_factory()
    user_info.update(override_data)

    payload = {"user": user_info}
    response = api_client.post("/users", payload=payload)

    _assert_error_response(
        response=response,
        expected_error_code=32,
        expected_message_snippet=expected_error_snippet,
        allowed_statuses=(200, 400, 422),
    )
    #An invalid contract response returns a status code (200) with the error message in the response body.
    #After resolving the inconsistency, remove the 200 status code from the allowed_statuses.


def test_update_user_validation_errors(api_client, created_user):
    invalid_payload = {
        "user": {
            "email": "not_an_email.com",
            "pic": "unsupported_pic_type",
        }
    }

    response = api_client.put(
        f"/users/{created_user['login']}",
        payload=invalid_payload,
        user_token=created_user["user_token"],
    )

    _assert_error_response(
        response=response,
        expected_error_code=32,
        expected_message_snippet="Email is not a valid email",
        allowed_statuses=(200, 400, 422),
    )
    _assert_error_response(
        response=response,
        expected_error_code=32,
        expected_message_snippet="is not a valid pic",
        allowed_statuses=(200, 400, 422),
    )
    #An invalid contract response returns a status code (200) with the error message in the response body.
    #After resolving the inconsistency, remove the 200 status code from the allowed_statuses.

def test_create_user_session_present_error(api_client, user_data_factory, created_user):
    second_user = user_data_factory()
    response = api_client.post(
        "/users",
        payload={"user": second_user},
        user_token=created_user["user_token"],
    )

    _assert_error_response(
        response=response,
        expected_error_code=31,
        expected_message_snippet="User session already present",
        allowed_statuses=(200, 400, 403),
    )
    # An invalid contract response returns a status code (200) with the error message in the response body.
    # After resolving the inconsistency, remove the 200 status code from the allowed_statuses.