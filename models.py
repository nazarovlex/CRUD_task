from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from database import Base
from pydantic import BaseModel


# requests models
class AddUserRequest(BaseModel):
    username: str
    email: str


class UpdateUserRequest(BaseModel):
    user_id: str
    username: str
    email: str


# postgres tables
class UsersTable(Base):
    __tablename__ = "users"
    user_uuid = Column(UUID, primary_key=True, unique=True)
    username = Column(String)
    email = Column(String, unique=True)
