import sys
import os

from litestar.testing import AsyncTestClient

# Add the project root (parent directory) to PYTHONPATH at runtime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from litestar.contrib.sqlalchemy.base import UUIDAuditBase
from sqlalchemy.ext.asyncio import async_sessionmaker



import pytest

# Create an in-memory SQLite database
DATABASE_URL = "sqlite+aiosqlite:///:memory:"
os.environ["connection_string"] = DATABASE_URL

from app.main import create_app, get_session_config
@pytest.fixture(scope="class")
def app():
    app = create_app()

    yield app


from app.config import get_engine

@pytest.fixture(scope="class")
async def async_session():
    engine = get_engine(DATABASE_URL)
    session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(UUIDAuditBase.metadata.create_all)
    yield session_factory
    await engine.dispose()

from app.models.user import User, provide_user_repo
from app.routes.auth import hash_password


@pytest.fixture(scope="class")
async def seed_db(async_session):
    async with async_session() as session:
        user_repo = await provide_user_repo(session)

        # Insert mock data into the database
        user = User(
            id="aaa3a8d4-d986-450a-bca6-21567ccbc63c",
            username="test_user",
            password=hash_password("password123"),
            displayname="Test User",
        )
        await user_repo.add(user)
        await session.commit()


@pytest.fixture(scope="class")
async def test_client(app):
    async with AsyncTestClient(app=app,session_config=get_session_config())  as client:
        yield client


