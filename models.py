from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, index=True, nullable=False)
    user_name = Column(String(50), unique=True, nullable=False)
    user_email = Column(String(50), unique=True, nullable=False)

class Jobs(Base):
    __tablename__ = "jobs"

    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    job_id = Column(Integer, primary_key=True, nullable=False)
    job_title = Column(String(50), unique=True, nullable=False)
    job_salary = Column(Integer, nullable=False)
