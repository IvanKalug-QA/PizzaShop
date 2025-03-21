from sqlalchemy import Column, String, Integer

from app.core.db import Base


class Pizza(Base):
    name = Column(String, nullable=False, unique=True)
    time = Column(Integer, nullable=False, )
