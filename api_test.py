import pytest
from main import app, validate_email
from fastapi.testclient import TestClient
from models import UsersTable
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# database settings
db_url = 'postgresql://postgres:postgres@postgres:5432/CRUD_task_DB'
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)


@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client


@pytest.mark.asyncio
async def test_handler_add_user(test_client):
    data = {
        "username": 'pytest',
        "email": "pytest@test.com"
    }

    response = test_client.post("/add_user", json=data)
    assert response.status_code == 201

    user_id = response.json()["user_id"]

    db = Session()
    user = db.query(UsersTable).filter(UsersTable.user_uuid == user_id).first()
    assert user is not None
    assert user.username == data["username"]
    assert user.email == data["email"]
    db.delete(user)
    db.commit()
    db.close()


@pytest.mark.asyncio
async def test_handler_delete_user(test_client):
    data = {
        "username": 'test_handler_delete_user',
        "email": "test_handler_delete_user@test.com"
    }

    add_user_response = test_client.post("/add_user", json=data)
    assert add_user_response.status_code == 201
    user_id = add_user_response.json()["user_id"]

    db = Session()

    user = db.query(UsersTable).filter(UsersTable.user_uuid == user_id).first()
    assert user is not None

    delete_user_response = test_client.delete(f"/delete_user?id={user_id}")
    assert delete_user_response.status_code == 200
    assert delete_user_response.json() == {"message": "user successfully deleted"}

    user = db.query(UsersTable).filter(UsersTable.user_uuid == user_id).first()
    assert user is None

    db.close()


@pytest.mark.asyncio
async def test_handler_update_user(test_client):
    data = {
        "username": 'test_handler_add_user',
        "email": "test_handler_add_user@test.com"
    }

    add_user_response = test_client.post("/add_user", json=data)
    assert add_user_response.status_code == 201
    user_id = add_user_response.json()["user_id"]

    db = Session()
    added_user = db.query(UsersTable).filter(UsersTable.user_uuid == user_id).first()

    assert added_user is not None
    assert added_user.username == data["username"]
    assert added_user.email == data["email"]
    db.close()
    new_data = {
        "user_id": user_id,
        "username": 'test_handler_update_user',
        "email": "test_handler_update_user@test.com"
    }
    update_user_response = test_client.put(f"/update_user", json=new_data)
    assert update_user_response.status_code == 201
    assert update_user_response.json() == {"message": "user successfully updated"}

    db = Session()
    updated_user = db.query(UsersTable).filter(UsersTable.user_uuid == user_id).first()

    assert updated_user is not None
    assert updated_user.username == new_data["username"]
    assert updated_user.email == new_data["email"]

    db.delete(updated_user)
    db.commit()
    db.close()


@pytest.mark.asyncio
async def test_handler_user_info(test_client):
    data = {
        "username": 'test_handler_add_user',
        "email": "test_handler_add_user@test.com"
    }

    add_user_response = test_client.post("/add_user", json=data)
    assert add_user_response.status_code == 201
    user_id = add_user_response.json()["user_id"]

    db = Session()
    added_user = db.query(UsersTable).filter(UsersTable.user_uuid == user_id).first()
    assert added_user is not None
    assert added_user.username == data["username"]
    assert added_user.email == data["email"]

    user_info_response = test_client.get(f"/user_data?id={user_id}")
    assert user_info_response.status_code == 200
    assert user_info_response.json()["user_data"]["username"] == added_user.username
    assert user_info_response.json()["user_data"]["email"] == added_user.email
    db.close()

    db = Session()
    user = db.query(UsersTable).filter(UsersTable.user_uuid == user_id).first()
    db.delete(user)
    db.commit()
    db.close()


@pytest.mark.asyncio
async def test_email_validator(test_client):
    email_1 = "qwe@gmail.com"
    valid_email = await validate_email(email_1)
    assert valid_email

    email_2 = "qwegmail.com"
    valid_email = await validate_email(email_2)
    assert not valid_email

    email_3 = "qwe@@gmail.com"
    valid_email = await validate_email(email_3)
    assert not valid_email

    email_4 = "qwe@gmailcom"
    valid_email = await validate_email(email_4)
    assert not valid_email

    email_5 = "qweasdqwbqwe"
    valid_email = await validate_email(email_5)
    assert not valid_email
