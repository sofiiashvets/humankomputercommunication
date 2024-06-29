from connection import Base
from sqlalchemy import Column, Integer, String, func, select
from sqlalchemy.orm import column_property, relationship

from model.Worker import Worker


class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, index=True, primary_key=True)
    name = Column(String)
    street = Column(String)
    city = Column(String)
    postcode = Column(String)
    
    workers_no = column_property(select(func.count(Worker.pesel)).where(Worker.department_id == id).scalar_subquery())

    worker = relationship("Worker", back_populates="department")

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True


