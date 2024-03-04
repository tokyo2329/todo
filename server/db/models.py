from sqlalchemy import Column, Integer, Boolean, String
from .database import Base


class Task(Base):
  __tablename__ = 'tasks'

  id = Column(Integer, primary_key = True)
  name = Column(String)
  is_done = Column(Boolean, default = False)
