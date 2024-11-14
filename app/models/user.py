from dataclasses import dataclass

from litestar.contrib.sqlalchemy.base import UUIDAuditBase
from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped


@dataclass
class AccountLogin:
    username: str
    password: str


class User(UUIDAuditBase):
    username: Mapped[str]
    displayname: Mapped[str]
    password: Mapped[str]


class UserRepository(SQLAlchemyAsyncRepository[User]):
    """User Repository"""

    model_type = User


async def provide_user_repo(db_session: AsyncSession) -> UserRepository:
    """This provides the default User repository"""
    return UserRepository(session=db_session)
