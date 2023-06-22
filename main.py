import uuid
import uvicorn
from fastapi import FastAPI
from fastapi.responses import Response
from models import UsersTable, AddUserRequest
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
async def add_user(user_data: AddUserRequest):
    user = {
        "user_uuid": str(uuid.uuid4()),
        "username": user_data.username,
        "email": user_data.email
    }

    db = SessionLocal()
    query = insert(UsersTable).values(**user)
    db.execute(query)
    db.commit()
    db.close()

    return {"message": "New user was added"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
