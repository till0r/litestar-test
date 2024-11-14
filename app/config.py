import os
from functools import lru_cache

from litestar.contrib.sqlalchemy.base import UUIDAuditBase
from litestar.contrib.sqlalchemy.plugins import (
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
)
from sqlalchemy.ext.asyncio import create_async_engine


@lru_cache
def get_engine(connection_string):

    # if you want to perform some dialect specific changes, do that here
    # otherwise just have a module level engine instead of this function
    # engine = create_async_engine(DB_URL_FROM_ENV)

    if connection_string == "sqlite+aiosqlite:///:memory:":
        return create_async_engine(connection_string, echo=True)
    return create_async_engine(connection_string)


# TODO: If no env, select the default database
if os.getenv("connection_string") is None:
    os.environ["connection_string"] = "sqlite+aiosqlite:///db.sqlite3"


connection_string = os.getenv("connection_string")

print(connection_string)

session_config = AsyncSessionConfig(expire_on_commit=False)
sqlalchemy_config = SQLAlchemyAsyncConfig(
    engine_instance=get_engine(connection_string),
    metadata=UUIDAuditBase.metadata,
    create_all=True,
    session_config=session_config,
)
