def create_user_and_login(client):
    import uuid
    email = f"{uuid.uuid4()}@example.com"

    client.post(
        "/auth/register",
        json={
            "email": email,
            "password": "12345678"
        }
    )

    response = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": "12345678"
        }
    )

    #print("LOGIN STATUS:", response.status_code)
    #print("LOGIN BODY:", response.json())

    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_todo_success(client):
    headers = create_user_and_login(client)

    response = client.post(
        "/todos/",
        json={
            "title": "Test todo",
            "description": "Test desc"
        },
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Test todo"


def test_create_todo_validation_fail(client):
    headers = create_user_and_login(client)

    response = client.post(
        "/todos/",
        json={
            "title": "",
        },
        headers=headers
    )

    assert response.status_code == 422


def test_get_todo_404(client):
    headers = create_user_and_login(client)

    response = client.get(
        "/todos/9999",
        headers=headers
    )

    assert response.status_code == 404


def test_create_todo_auth_fail(client):
    response = client.post(
        "/todos/",
        json={
            "title": "No auth"
        }
    )

    assert response.status_code == 401