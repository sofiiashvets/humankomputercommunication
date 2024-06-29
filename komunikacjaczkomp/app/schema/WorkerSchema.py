from typing import List, Optional
from pydantic import BaseModel

from schema.Child import Child
from schema.DepartmentsSchema import DepartmentsSchema
from schema.SalarySchema import SalarySchema


class WorkerSchema(BaseModel):
    pesel: str
    imie: str
    nazwisko: str
    age: int
    criminal_record: bool
    children: Optional[List[Child]]
    salary: Optional[List[SalarySchema]]
    department: Optional[DepartmentsSchema]
    class Config:
        arbitrary_types_allowed = True
        orm_mode = True


class AddWorkerSchema(BaseModel):
    pesel: str
    imie: str
    nazwisko: str
    age: int
    criminal_record: bool
    department_id: int
    class Config:
        arbitrary_types_allowed = True
        orm_mode = True
