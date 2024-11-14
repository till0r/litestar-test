import pytest
from litestar.status_codes import HTTP_200_OK, HTTP_302_FOUND


@pytest.mark.asyncio
@pytest.mark.usefixtures("app", "seed_db")
class TestHomeRoute:
    async def test_get_home_anonymous(self, test_client):
        await test_client.set_session_data({"a": "b"})
        response = await test_client.get(
            "/",
            follow_redirects=False,
        )

        assert response.status_code == HTTP_302_FOUND
        assert response.headers.get("Location") == "/login"

    async def test_get_home_authenticated(self, test_client):
        await test_client.set_session_data({"username": "test_user"})
        response = await test_client.get(
            "/",
            follow_redirects=False,
        )

        assert response.status_code == HTTP_200_OK
        assert "Hello" in response.text
