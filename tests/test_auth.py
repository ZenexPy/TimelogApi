import json
import pytest

from httpx import AsyncClient
from sqlalchemy import select, Result
from ..src.core.models.position import Position
from ..src.core.models.user import User
from .conftest import async_session_maker


async def test_create_position_db():
    async with async_session_maker() as session:
        new_position = Position(id=1, title="Python Dev",
                                description="Backend Dev", salary=50000)
        session.add(new_position)
        await session.commit()

        stmt = select(Position).order_by(Position.id)
        result: Result = await session.execute(stmt)
        position = result.scalars().first()
        assert (position.id, position.title, position.description, position.salary) == \
            (1, "Python Dev", "Backend Dev", 50000), "Роль не добавилась"


async def test_register(client: AsyncClient):
    user_data = {
        "email": "mail@mail.com",
        "username": "string",
        "password": "string",
        "position_fk": 1
    }
    response = await client.post("/users/register", data=json.dumps(user_data))
    data_from_response = response.json()
    assert response.status_code == 201
    assert data_from_response["email"] == user_data["email"]
    assert data_from_response["username"] == user_data["username"]
    assert data_from_response["position_fk"] == user_data["position_fk"]

    async with async_session_maker() as session:
        stmt = select(User)
        result: Result = await session.execute(stmt)
        user1 = result.scalars().first()

    assert user1.id == 1
    assert user1.email == user_data["email"]
    assert user1.position_fk == user_data["position_fk"]
    assert user1.username == user_data["username"]
    assert user1.is_active == True
    assert user1.is_superuser == False
    assert user1.is_verified == False


@pytest.mark.parametrize("user_data_, expected_status_code", [
    ({"email": "mail@mail.com", "username": "username",
     "password": "password", "position_fk": 1}, 201),
    ({"email": "invalid_email", "username": "username", "password": "password",
     "position_fk": "string"}, 422),
    ({"email": "mail@mail.com", "username": 123, "password": "password",
     "position_fk": 1}, 422), 
    ({"email": "mail@mail.com", "username": "username", "password": 123,
     "position_fk": 1}, 422),  
    ({"email": "invalid_email", "username": "",
     "password": "password", "position_fk": 1}, 422), 
    ({"email": "new@mail.com", "username": "username",
     "password": "password", "position_fk": 0}, 422),  
])
async def test_user_register_errors(client: AsyncClient, user_data_, expected_status_code):
    response = await client.post("/users/register", data=json.dumps(user_data_))
    assert response.status_code == expected_status_code
