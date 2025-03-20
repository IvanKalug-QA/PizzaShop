from sqlalchemy import Column, String

from app.core.db import Base


class Pizza(Base):
    name = Column(String, nullable=False, unique=True)
    time = Column(String, nullable=False, )
