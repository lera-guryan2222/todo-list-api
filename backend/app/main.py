from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Todo List API", description="API для управления задачами", version="1.0.0"
)


@app.get("/")
async def root():
    return {"message": "Todo List API", "version": "1.0.0"}


@app.get("/health/")
async def health_check(db: Annotated[Session, Depends(get_db)]):
    try:
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception:
        return {"status": "unhealthy", "database": "disconnected"}


@app.post("/tasks/", response_model=schemas.Task, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: schemas.TaskCreate, db: Annotated[Session, Depends(get_db)]
):
    return crud.TaskCRUD.create_task(db=db, task=task)


@app.get("/tasks/", response_model=list[schemas.Task])
async def read_tasks(
    db: Annotated[Session, Depends(get_db)],
    skip: int = 0,
    limit: int = 100,
    completed: bool | None = None,
    priority: str | None = None,
):
    return crud.TaskCRUD.get_tasks(
        db=db, skip=skip, limit=limit, completed=completed, priority=priority
    )


@app.get("/tasks/{task_id}", response_model=schemas.Task)
async def read_task(task_id: int, db: Annotated[Session, Depends(get_db)]):
    db_task = crud.TaskCRUD.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return db_task


@app.put("/tasks/{task_id}", response_model=schemas.Task)
async def update_task(
    task_id: int,
    task_update: schemas.TaskUpdate,
    db: Annotated[Session, Depends(get_db)],
):
    db_task = crud.TaskCRUD.update_task(db, task_id=task_id, task_update=task_update)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return db_task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, db: Annotated[Session, Depends(get_db)]):
    deleted = crud.TaskCRUD.delete_task(db, task_id=task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return None
