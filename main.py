import uvicorn
from fastapi import FastAPI, Query, UploadFile, File, Form
from database import database, engine, Base, SessionLocal

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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
