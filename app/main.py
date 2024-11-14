import os
from functools import lru_cache

from dotenv import load_dotenv
from litestar import Litestar
from litestar.type import EmptyType
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyInitPlugin
from litestar.exceptions import NotAuthorizedException
from litestar.middleware.session.server_side import (
    ServerSideSessionBackend,
    ServerSideSessionConfig,
)
from litestar.security.session_auth import SessionAuth
from litestar.static_files import create_static_files_router
from litestar.template.config import TemplateConfig
from app.config import sqlalchemy_config
from app.models.user import User
from app.routes.auth import (
    auth_redirect_handler,
    get_login_handler,
    post_login_handler,
    post_logout_handler,
    retrieve_user_handler,
)
from app.routes.home import home


@lru_cache
def get_session_config() -> ServerSideSessionConfig:
    return ServerSideSessionConfig()


@lru_cache
def get_session_auth() -> SessionAuth:
    return SessionAuth[User, ServerSideSessionBackend](
        session_backend_config=get_session_config(),
        retrieve_user_handler=retrieve_user_handler,
        exclude=["/login", "/schema"],
    )


def create_app() -> Litestar:
    # Read environment variables
    load_dotenv()
    debug = os.getenv("DEBUG", "false").lower() == "true"

    # Configure Jinja2 template engine
    template_config = TemplateConfig(directory="templates", engine=JinjaTemplateEngine)

    # Create the Litestar app instance
    app = Litestar(
        route_handlers=[
            home,
            get_login_handler,
            post_login_handler,
            post_logout_handler,
            create_static_files_router(path="static", directories=["static"]),
        ],
        middleware=[get_session_auth().middleware],
        template_config=template_config,
        signature_types=[EmptyType],
        exception_handlers={NotAuthorizedException: auth_redirect_handler},
        debug=debug,  # Pass the debug flag
        plugins=[SQLAlchemyInitPlugin(config=sqlalchemy_config)],
    )

    return app
