from fastapi import FastAPI, Depends
from sqlalchemy.orm.session import Session
from db import models, schemas, crud
from db.database import engine, SessionLocal

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

@app.get('/tasks', response_model=list[schemas.Task])
def get_tasks(db: Session = Depends(get_db)):
  _tasks = crud.get_tasks(db=db)
  return _tasks

@app.get('/tasks/{task_id}', response_model=schemas.Task)
def get_task(task_id: int, db: Session = Depends(get_db)):
  _task = crud.get_task(db=db, task_id=task_id)
  return _task

@app.post('/tasks', response_model=schemas.Task)
def create_task(task: schemas.Task, db: Session = Depends(get_db)):
  _task = crud.create_task(db=db, task=task)
  return _task

@app.put('/tasks/{task_id}', response_model=schemas.Task)
def update_task(task_id: int, task: schemas.Task, db: Session = Depends(get_db)):
  _task = crud.update_task(db=db, task_id=task_id, task=task)
  return _task

@app.delete('/tasks/{task_id}', response_model=schemas.Task)
def delete_task(task_id: int, db: Session = Depends(get_db)):
  _task = crud.delete_task(db=db, task_id=task_id)
  return _task
