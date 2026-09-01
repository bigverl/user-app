class TestLogin:
    def test_correct_credentials_returns_token(self, client):
        client.post(
            "/users/",
            json={
                "username": "dave",
                "email": "dave@example.com",
                "password": "pw123",
            },
        )
        response = client.post(
            "/token/", data={"username": "dave", "password": "pw123"}
        )
        assert response.status_code == 200
        body = response.json()
        assert body["token_type"] == "bearer"
        assert "access_token" in body

    def test_wrong_password_returns_401(self, client):
        client.post(
            "/users/",
            json={
                "username": "dave",
                "email": "dave@example.com",
                "password": "pw123",
            },
        )
        response = client.post(
            "/token/", data={"username": "dave", "password": "wrong"}
        )
        assert response.status_code == 401

    def test_unknown_username_returns_401(self, client):
        response = client.post(
            "/token/", data={"username": "nobody", "password": "whatever"}
        )
        assert response.status_code == 401

    def test_missing_fields_returns_422(self, client):
        response = client.post("/token/", data={"username": "dave"})
        assert response.status_code == 422
