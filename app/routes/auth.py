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

