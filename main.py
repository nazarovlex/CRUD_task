import uuid
import uvicorn
from fastapi import FastAPI, Query
from fastapi.responses import Response
from models import UsersTable, AddUserRequest, UpdateUserRequest
from database import database, engine, Base, SessionLocal
from sqlalchemy.dialects.postgresql import insert

# FastAPI init
app = FastAPI()


# create tables in DB
async def create_tables():
    # create tables if not exist
    Base.metadata.create_all(bind=engine)


# create DB connection
@app.on_event("startup")
async def startup():
    await database.connect()
    await create_tables()


# close DB connection
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/add_user", status_code=201)
async def add_user(response: Response, user_data: AddUserRequest):
    # take request data
    user = {
        "user_uuid": str(uuid.uuid4()),
        "username": user_data.username,
        "email": user_data.email
    }

    # DB session init
    db = SessionLocal()

    # create query for postgre
    query = insert(UsersTable).values(**user)

    # exception handling of DB insertion
    try:
        db.execute(query)
    except Exception as error:
        db.rollback()
        db.close()
        response.status_code = 500
        return {"error": f"add new user failed, error: {error}"}

    # commit changes in DB and close session
    db.commit()
    db.close()

    return {"message": f"New user was added", "user_id": user['user_uuid']}


@app.put("/update_user", status_code=201)
async def update_user(response: Response, user_data: UpdateUserRequest):
    # take request data
    user = {
        "user_uuid": user_data.user_id,
        "username": user_data.username,
        "email": user_data.email
    }

    # DB session init
    db = SessionLocal()

    old_user_data = db.query(UsersTable).filter(UsersTable.user_uuid == user_data.user_id).one()
    if not old_user_data:
        db.close()
        response.status_code = 400
        return {"error": f"can't find user with id: {user_data.user_id}"}

    try:
        for key, value in user.items():
            setattr(old_user_data, key, value)
    except Exception as error:
        db.close()
        response.status_code = 500
        return {"error": f"can't update user, error: {error}"}

    # commit changes in DB and close session
    db.commit()
    db.close()

    return {"message": "user successfully updated"}


@app.delete("/delete_user", status_code=200)
async def delete_user(response: Response, id: str = Query(description="id")) -> dict:
    # DB session init
    db = SessionLocal()

    # exception handling of wrong user id and delete user
    try:
        user = db.query(UsersTable).filter(UsersTable.user_uuid == id).one()
        db.delete(user)
    except Exception as error:
        db.close()
        response.status_code = 400
        return {"error": f"can't find user with id:{id}, error: {error}"}

    # commit changes and close DB
    db.commit()
    db.close()

    return {"message": "user successfully deleted"}


@app.get("/user_data", status_code=200)
async def delete_user(response: Response, id: str = Query(description="id")) -> dict:

    # DB session init
    db = SessionLocal()

    # exception handling of wrong user id and delete user
    try:
        user_DB = db.query(UsersTable).filter(UsersTable.user_uuid == id).first()
    except Exception as error:
        db.close()
        response.status_code = 400
        return {"error": f"can't find user with id:{id}, error: {error}"}

    user_data = {
        "user_uuid": user_DB.user_uuid,
        "username": user_DB.username,
        "email": user_DB.email
    }

    # commit changes and close DB
    db.commit()
    db.close()

    return {"user_data": user_data}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
