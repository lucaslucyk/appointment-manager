from enum import Enum, unique
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum as SAEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null
from sqlalchemy_utils import EmailType
from app.db.base_class import Base
from .mixins import Timestamp

class Role(Enum):
    professional = 1
    consumer = 2


class User(Timestamp, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(EmailType, unique=True, index=True, nullable=False)
    password = Column(String(100), nullable=False)
    is_active = Column(Boolean(), default=True)
    role = Column(SAEnum(Role))

    profile = relationship("Profile", back_populates="owner", uselist=False)


class Profile(Timestamp, Base):
    __tablename__ = "profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="profile")