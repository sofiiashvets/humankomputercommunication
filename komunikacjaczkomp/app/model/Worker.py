from connection import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship


class Worker(Base):
    __tablename__ = 'workers'
    pesel = Column(String, index=True, primary_key=True)
    imie = Column(String)
    nazwisko = Column(String)
    age = Column(Integer)
    criminal_record = Column(Boolean)
    children = Column(JSONB, default=dict())
    department_id = Column(Integer, ForeignKey("departments.id"))

    
    department = relationship("Department", back_populates="worker")
    salary = relationship(
        "Salary", back_populates="worker", cascade="all, delete")
