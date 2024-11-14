from unittest.mock import MagicMock, Mock

import pytest
from litestar import Request
from litestar.contrib.htmx.request import HTMXRequest
from litestar.contrib.htmx.response import ClientRedirect
from litestar.exceptions import NotAuthorizedException, PermissionDeniedException
from litestar.response import Redirect
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_302_FOUND
from litestar.testing import AsyncTestClient

from app.main import create_app
from app.routes.auth import auth_redirect_handler


@pytest.fixture(scope="function")
def exception():
    return PermissionDeniedException()


@pytest.fixture(scope="function")
def htmx_request():
    return MagicMock(spec=HTMXRequest)


@pytest.fixture(scope="function")
def regular_request():
    return MagicMock(spec=Request)


@pytest.fixture
def mock_route_handler():
    # This can be any route handler you would normally pass
    async def handler(connection) -> None:
        return None

    return handler


@pytest.fixture
def mock_asgi_connection():
    """Fixture to mock ASGIConnection"""
    connection = Mock()
    connection.scope = {"session": {}}
    return connection


class TestAuthRedirectHandler:
    def test_http_redirect(self):
        request = Mock(spec=Request)
        exc = NotAuthorizedException()
        response = auth_redirect_handler(request, exc=exc)

        assert isinstance(response, Redirect)

    def test_htmx_redirect(self):
        request = Mock(spec=HTMXRequest)
        exc = NotAuthorizedException()
        response = auth_redirect_handler(request, exc=exc)

        assert isinstance(response, ClientRedirect)


@pytest.mark.asyncio
@pytest.mark.usefixtures("seed_db")
class TestLoginRoute:
    async def test_post_login_valid(self, test_client):
        test_form_data = {
            "username": "test_user",
            "password": "password123",
        }
        response = await test_client.post(
            "/login",
            headers={"HX-Request": "true"},
            data=test_form_data,
        )
        assert response.status_code == HTTP_201_CREATED
        assert response.headers.get("HX-Redirect") == "/"

    async def test_post_login_invalid_password(self, test_client):
        test_form_data = {
            "username": "test_user",
            "password": "password1234",
        }
        response = await test_client.post(
            "/login",
            data=test_form_data,
        )
        assert response.status_code == HTTP_200_OK
        assert "Log in" in response.text

    async def test_post_login_invalid_user(self, test_client):
        test_form_data = {
            "username": "test_user_2",
            "password": "password123",
        }
        response = await test_client.post(
            "/login",
            data=test_form_data,
        )
        assert response.status_code == HTTP_200_OK
        assert "Log in" in response.text

    async def test_get_login(self):
        async with AsyncTestClient(app=create_app()) as client:
            response = await client.get("/login")
            assert response.status_code == HTTP_200_OK
            assert "Log in" in response.text


@pytest.mark.asyncio
@pytest.mark.usefixtures("seed_db")
class TestLogout:
    async def test_logout(self, test_client):
        test_form_data = {
            "username": "test_user",
            "password": "password123",
        }
        await test_client.post(
            "/login",
            data=test_form_data,
        )
        response = await test_client.post("/logout")

        assert response.status_code == HTTP_201_CREATED
        assert response.headers.get("HX-Redirect") == "/login"
