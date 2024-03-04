from sqlalchemy.orm import Session
from . import models, schemas


def get_tasks(db: Session):
  _task = db.query(models.Task).all()
  return _task

def get_task(db: Session, task_id: int) -> models.Task:
  _task = db.query(models.Task).filter(models.Task.id == task_id).first()
  return _task

def create_task(db: Session, task: schemas.TaskCreate):
  _task = models.Task(name=task.name)
  db.add(_task)
  db.commit()
  return _task

def update_task(db: Session, task_id: int, task: schemas.TaskUpdate):
  _task = get_task(db, task_id)
  _task.name = task.name
  _task.is_done = task.is_done
  db.add(_task)
  db.commit()
  return _task

def delete_task(db: Session, task_id):
  _task = get_task(db, task_id)
  db.delete(_task)
  db.commit()
  return _task
