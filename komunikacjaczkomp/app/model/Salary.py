from connection import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Salary(Base):
    __tablename__ = 'salary'
    id = Column(Integer, index=True, primary_key=True)
    worker_pesel = Column(String, ForeignKey('workers.pesel'))
    month = Column(Integer)
    amount = Column(Integer)

    worker = relationship(
        "Worker", back_populates="salary", cascade="all, delete")

    def __repr__(self):
        return f"Id = {self.id}, month = {self.month}, amount = {self.amount} \n"
