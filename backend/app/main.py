from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas, crud
from .database import engine, get_db
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Todo List API",
    description="API для управления задачами",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Todo List API", "version": "1.0.0"}

@app.get("/tasks/", response_model=List[schemas.Task])
async def read_tasks(
    skip: int = 0,
    limit: int = 100,
    completed: Optional[bool] = None,
    priority: Optional[schemas.PriorityEnum] = None,
    db: Session = Depends(get_db)
):
    """
    Получить список всех задач с возможностью фильтрации
    """
    tasks = crud.TaskCRUD.get_tasks(db, skip=skip, limit=limit, completed=completed, priority=priority)
    return tasks

@app.get("/tasks/{task_id}", response_model=schemas.Task)
async def read_task(task_id: int, db: Session = Depends(get_db)):
    """
    Получить задачу по ID
    """
    db_task = crud.TaskCRUD.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return db_task

@app.post("/tasks/", response_model=schemas.Task, status_code=status.HTTP_201_CREATED)
async def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    """
    Создать новую задачу
    """
    return crud.TaskCRUD.create_task(db=db, task=task)

@app.put("/tasks/{task_id}", response_model=schemas.Task)
async def update_task(
    task_id: int, 
    task_update: schemas.TaskUpdate, 
    db: Session = Depends(get_db)
):
    """
    Обновить существующую задачу
    """
    db_task = crud.TaskCRUD.update_task(db, task_id=task_id, task_update=task_update)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return db_task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    """
    Удалить задачу
    """
    deleted = crud.TaskCRUD.delete_task(db, task_id=task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return None

@app.get("/health/")
async def health_check(db: Session = Depends(get_db)):
    """
    Проверка работоспособности сервиса
    """
    try:
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}