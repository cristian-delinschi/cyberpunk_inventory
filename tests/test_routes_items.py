import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.main import app  # Import your FastAPI app
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate
from app.crud.item import create_item, get_item, get_items, update_item, delete_item
from app.db.database import get_db_session, Base

# Define an SQLite in-memory database for testing
DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create a new SQLAlchemy engine and session for testing
engine = create_async_engine(DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)


async def override_get_db():
    async with TestingSessionLocal() as session:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield session


app.dependency_overrides[get_db_session] = override_get_db


# Initialize the database
@pytest.fixture(scope="module")
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# Initialize the TestClient
client = TestClient(app)

import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your_secret_key"  # Replace with your actual secret key
ALGORITHM = "HS256"


def create_test_token():
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode = {"exp": expire, "sub": "testuser"}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@pytest.fixture
def test_token():
    return create_test_token()


@pytest.mark.asyncio
async def test_create_item(test_token):
    async with TestingSessionLocal() as db:
        item_data = {
            "name": "Test Item",
            "description": "A test item description",
            "category": "Test Category",
            "quantity": 10,
            "price": 99
        }
        response = client.post(
            "/items/", data=item_data, headers={"Authorization": f"Bearer {test_token}"}

        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test Item"


@pytest.mark.asyncio
async def test_get_item(test_token):
    async with TestingSessionLocal() as db:
        item_data = ItemCreate(
            name="Test Item",
            description="A test item description",
            category="Test Category",
            quantity=10,
            price=99
        )
        await create_item(db, item_data)

        response = client.get("/items/1/", headers={"Authorization": f"Bearer {test_token}"})
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Item"


@pytest.mark.asyncio
async def test_get_items(test_token):
    async with TestingSessionLocal() as db:
        # Create multiple items first
        item_data1 = ItemCreate(
            name="Item 1",
            description="Description 1",
            category="Category 1",
            quantity=5,
            price=20.00
        )
        item_data2 = ItemCreate(
            name="Item 2",
            description="Description 2",
            category="Category 2",
            quantity=15,
            price=30.00
        )
        await create_item(db, item_data1)
        await create_item(db, item_data2)

        response = client.get(
            "/items/", params={"limit": 10, "offset": 0},
            headers={"Authorization": f"Bearer {test_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2


@pytest.mark.asyncio
async def test_update_item(test_token):
    async with TestingSessionLocal() as db:
        # Create an item first
        item_data = ItemCreate(
            name="Old Item",
            description="Old description",
            category="Old category",
            quantity=1,
            price=1.00
        )
        created_item = await create_item(db, item_data)

        update_data = ItemUpdate(
            name="Updated Item",
            description="Updated description"
        )
        response = client.put(
            f"/items/{created_item['id']}/", json=update_data.dict(),
            headers={"Authorization": f"Bearer {test_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Item"


@pytest.mark.asyncio
async def test_delete_item(test_token):
    async with TestingSessionLocal() as db:
        # Create an item first
        item_data = ItemCreate(
            name="Item to delete",
            description="Description",
            category="Category",
            quantity=1,
            price=1.00
        )
        created_item = await create_item(db, item_data)

        response = client.delete(
            f"/items/{created_item['id']}/",
            headers={"Authorization": f"Bearer {test_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Item to delete"

        # Verify item is deleted
        response = client.get(
            f"/items/{created_item['id']}/",
            headers={"Authorization": f"Bearer {test_token}"}
        )
        assert response.status_code == 404
