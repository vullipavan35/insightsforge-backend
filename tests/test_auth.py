def test_user_registration_and_login(client):
    # 1. Register a new user
    register_payload = {
        "email": "testuser@insightsforge.io",
        "password": "strongPassword123",
        "full_name": "Test Engineer",
    }
    response = client.post("/api/v1/auth/register", json=register_payload)
    assert response.status_code == 201
    reg_data = response.json()
    assert "access_token" in reg_data
    assert reg_data["token_type"] == "bearer"
    assert reg_data["user"]["email"] == "testuser@insightsforge.io"

    # 2. Login with valid credentials
    login_payload = {
        "email": "testuser@insightsforge.io",
        "password": "strongPassword123",
    }
    response = client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 200
    login_data = response.json()
    assert "access_token" in login_data
    token = login_data["access_token"]

    # 3. Access protected /auth/me route
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == 200
    me_data = response.json()
    assert me_data["email"] == "testuser@insightsforge.io"
    assert me_data["full_name"] == "Test Engineer"
