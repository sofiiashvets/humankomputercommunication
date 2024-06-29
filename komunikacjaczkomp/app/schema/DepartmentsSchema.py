from typing import Optional

from pydantic import BaseModel

# TODO


class DepartmentsSchema(BaseModel):
    id: Optional[int]
    name: Optional[str]
    street: Optional[str]
    city: Optional[str]
    postcode: Optional[str]
    workers_no: Optional[int]
    workers_no = 0

    def __repr__(self):
        return f" name = {self.name}, street = {self.street}, city = {self.city}, postcode = {self.postcode}, workers_no = {self.workers_no} \n"

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True
