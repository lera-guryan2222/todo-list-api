from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime
from typing import List, Optional

class TaskCRUD:
    @staticmethod
    def get_task(db: Session, task_id: int) -> Optional[models.Task]:
        return db.query(models.Task).filter(models.Task.id == task_id).first()

    @staticmethod
    def get_tasks(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        completed: Optional[bool] = None,
        priority: Optional[schemas.PriorityEnum] = None
    ) -> List[models.Task]:
        query = db.query(models.Task)
        
        if completed is not None:
            query = query.filter(models.Task.completed == completed)
        
        if priority:
            query = query.filter(models.Task.priority == priority)
        
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def create_task(db: Session, task: schemas.TaskCreate) -> models.Task:
        db_task = models.Task(**task.model_dump())
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task

    @staticmethod
    def update_task(
        db: Session, 
        task_id: int, 
        task_update: schemas.TaskUpdate
    ) -> Optional[models.Task]:
        db_task = TaskCRUD.get_task(db, task_id)
        if not db_task:
            return None
        
        update_data = task_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_task, field, value)
        
        db.commit()
        db.refresh(db_task)
        return db_task

    @staticmethod
    def delete_task(db: Session, task_id: int) -> bool:
        db_task = TaskCRUD.get_task(db, task_id)
        if not db_task:
            return False
        
        db.delete(db_task)
        db.commit()
        return True