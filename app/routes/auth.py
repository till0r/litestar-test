from typing import Annotated, Any, Dict, Optional

import bcrypt
from litestar import get, post
from litestar.connection import ASGIConnection
from litestar.connection.request import Request
from litestar.contrib.htmx.request import HTMXRequest
from litestar.contrib.htmx.response import ClientRedirect, HTMXTemplate
from litestar.di import Provide
from litestar.enums import RequestEncodingType
from litestar.exceptions import HTTPException
from litestar.params import Body
from litestar.response import Redirect

from app.config import sqlalchemy_config
from app.models.user import AccountLogin, User, UserRepository, provide_user_repo


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


async def retrieve_user_handler(
    session: Dict[str, Any], connection: ASGIConnection[Any, Any, Any, Any]
) -> Optional[User]:
    username = session.get("username")
    if username is None:
        return None

    # NOTE: Since we are using server side sessions, there is no actual need to get the user
    # from the database - we can trust the username we wrote into the session.
    user_repo = await provide_user_repo(
        sqlalchemy_config.provide_session(connection.app.state, connection.scope)
    )
    return await user_repo.get_one_or_none(username=username)


def auth_redirect_handler(
    request: Request | HTMXRequest, exc: HTTPException
) -> Redirect | ClientRedirect:
    if isinstance(request, HTMXRequest):
        return ClientRedirect("/login")
    else:
        return Redirect("/login")


@get("/login", sync_to_thread=False)
def get_login_handler() -> HTMXTemplate:
    return HTMXTemplate(template_name="login.html")


@post("/login", dependencies={"user_repo": Provide(provide_user_repo)})
async def post_login_handler(
    request: HTMXRequest,
    data: Annotated[AccountLogin, Body(media_type=RequestEncodingType.URL_ENCODED)],
    user_repo: UserRepository,
) -> HTMXTemplate | ClientRedirect:
    def render_invalid_credentials(data):
        return HTMXTemplate(
            template_name="login.html",
            context={
                "username": data.username,
                "password": data.password,
                "error": "invalid_credentials",
            },
        )

    user = await user_repo.get_one_or_none(username=data.username)
    if not user:
        return render_invalid_credentials(data)

    stored_password_hash = user.password.encode("utf-8")
    if not bcrypt.checkpw(data.password.encode("utf-8"), stored_password_hash):
        return render_invalid_credentials(data)

    request.session["username"] = user.username
    request.session["displayname"] = user.displayname

    return ClientRedirect(redirect_to="/")


@post("/logout")
async def post_logout_handler(request: HTMXRequest) -> ClientRedirect:
    request.clear_session()
    return ClientRedirect("/login")
