from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal
from typing import Annotated, List
from pydantic import BaseModel

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class UserBase(BaseModel):
    user_name: str
    user_email: str

class UserBaseModel(BaseModel):
    id: int

    class Config:
        orm_mode = True

class JobBase(BaseModel):
    user_id: int
    job_title: str
    job_salary: int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    return {"message":"User created successfully"}

@app.get("/users/{userId}", response_model=UserBase, status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: int, db: db_dependency):
    get_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if get_user is None:
        raise HTTPException(status_code=404, detail="User not found!")
    return get_user

@app.post("/jobs/", status_code=status.HTTP_201_CREATED)
async def create_job(job: JobBase, db: db_dependency):
    new_job = models.Jobs(**job.model_dump())
    db.add(new_job)
    db.commit()
    return {"message": "Job Created Successfully"}

@app.get("/jobs/", response_model=List[JobBase], status_code=status.HTTP_200_OK)
async def fetch_jobs(db: db_dependency):
    jobs = db.query(models.Jobs).all()
    return jobs

