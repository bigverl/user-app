from app.auth.dependencies import get_current_user
from app.main import app


class TestCreate:
    def test_create_returns_201(self, client):
        response = client.post(
            "/users/",
            json={
                "username": "dave",
                "email": "dave@example.com",
                "password": "pw123",
            },
        )
        print(response)
        assert response.status_code == 201
        body = response.json()
        assert body["username"] == "dave"
        assert body["role"] == "viewer"
        assert "hashed_password" not in body

    def test_create_missing_field_returns_422(self, client):
        response = client.post("/users/", json={"email": "dave@example.com"})
        assert response.status_code == 422


class TestGetList:
    def test_returns_all(self, client):
        response = client.get("/users/")
        assert response.status_code == 200
        assert len(response.json()) == 3


class TestGetOne:
    def test_found_returns_200(self, client):
        response = client.get("/users/1")
        assert response.status_code == 200
        assert response.json()["username"] == "admin_user"

    def test_missing_returns_404(self, client):
        response = client.get("/users/999")
        assert response.status_code == 404


class TestUpdate:
    def test_update_returns_200(self, client):
        response = client.patch("/users/1", json={"username": "new_name"})
        assert response.status_code == 200
        assert response.json()["username"] == "new_name"

    def test_missing_returns_404(self, client):
        response = client.patch("/users/999", json={"username": "new_name"})
        assert response.status_code == 404


class TestUpdateRoleGuard:
    def test_admin_can_change_role(self, client):
        app.dependency_overrides[get_current_user] = lambda: 1  # admin_user seed id
        response = client.patch("/users/2", json={"role": "admin"})
        assert response.status_code == 200
        assert response.json()["role"] == "admin"

    def test_non_admin_cannot_change_role(self, client):
        app.dependency_overrides[get_current_user] = lambda: 2  # editor_user seed id
        response = client.patch("/users/1", json={"role": "admin"})
        assert response.status_code == 403


class TestDelete:
    def test_delete_returns_204(self, client):
        response = client.delete("/users/1")
        assert response.status_code == 204

    def test_missing_returns_404(self, client):
        response = client.delete("/users/999")
        assert response.status_code == 404
