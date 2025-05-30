from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import SessionLocal, KPITarget, Assignment
from pydantic import BaseModel
from datetime import date
from typing import List

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class KPITargetCreate(BaseModel):
    title: str
    description: str
    target_value: float
    unit: str
    deadline: date

@router.post("/kpi-targets/")
def create_kpi_target(kpi: KPITargetCreate, db: Session = Depends(get_db)):
    new_target = KPITarget(**kpi.dict())
    db.add(new_target)
    db.commit()
    db.refresh(new_target)
    return new_target

@router.get("/kpi-targets/", response_model=List[KPITargetCreate])
def list_kpi_targets(db: Session = Depends(get_db)):
    return db.query(KPITarget).all()

class AssignmentCreate(BaseModel):
    user_id: int
    target_id: int
    assigned_date: date

@router.post("/assign-target/")
def assign_kpi(assign: AssignmentCreate, db: Session = Depends(get_db)):
    assignment = Assignment(**assign.dict())
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment
