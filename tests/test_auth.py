def test_register_success(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "newuser@example.com",
            "password": "12345678"
        }
    )

    assert response.status_code == 200  


def test_login_success(client):
    client.post(
        "/auth/register",
        json={
            "email": "loginuser@example.com",
            "password": "12345678"
        }
    )

    response = client.post(
        "/auth/login",
        data={   
            "username": "loginuser@example.com", 
            "password": "12345678"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()