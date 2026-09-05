import time

from fastapi.testclient import TestClient

from app.events.models import UserCreatedEvent
from app.main import app


class TestRealDispatcherWiring:
    def test_creating_a_user_fires_a_handler_via_app_state_dispatcher(self):
        received = []

        async def handler(event):
            received.append(event)

        with TestClient(app) as client:
            app.state.dispatcher.subscribe(UserCreatedEvent, handler)

            response = client.post(
                "/users/",
                json={
                    "username": "dave",
                    "email": "dave@example.com",
                    "password": "pw123",
                },
            )
            assert response.status_code == 201

            time.sleep(0.05)

        assert len(received) == 1
        assert received[0].user_id == response.json()["user_id"]
