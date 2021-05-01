from sqlalchemy import Column, Integer, String
from database import Base


class AppUser(Base):
    __tablename__ = 'app_user'

    id = Column(Integer, primary_key=True)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), unique=True, nullable=False)
