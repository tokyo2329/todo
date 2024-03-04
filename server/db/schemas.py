from pydantic import BaseModel


class TaskBase(BaseModel):
  name: str

class TaskCreate(TaskBase):
  pass

class TaskRead(TaskBase):
  id: int
  is_done: bool

  class Config:
    orm_mode = True

class TaskUpdate(TaskBase):
  is_done: bool
