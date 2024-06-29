from typing import List

from model.Department import Department
from model.Worker import Worker
from schema.DepartmentsSchema import DepartmentsSchema
from sqlalchemy.orm import Session

#####################


class CRUDDepartment:

    # TODO
    def get_all_by_name(self, db: Session, q: str) -> List[DepartmentsSchema]:
        items = db.query(Department).filter(Department.name == q).all()
        return items

    def get_by_id(self, db: Session, department_id: int) -> DepartmentsSchema:
        item = db.query(Department).filter(
            Department.id == department_id).first()
        if (item):
            return item

    def delete_department_by_id(self, db: Session, department_id: int) -> bool:
        self.set_none_department_for_workers_in_department(
            db=db, department_id=department_id)
        department_to_delete = db.query(Department).filter(
            Department.id == department_id).one()
        if department_to_delete:
            db.delete(department_to_delete)
            db.commit()
            return True
        return False

    def get_all(self, db: Session) -> List[DepartmentsSchema]:
        items = db.query(Department).limit(1000).all()
        return items

    def add_department(self, db: Session, data: Department) -> DepartmentsSchema:
        new_department = Department()
        new_department.name = data.name
        new_department.street = data.street
        new_department.city = data.city
        new_department.postcode = data.postcode
        db.add(new_department)
        db.commit()
        return new_department

    def update(self, db: Session, data: Department) -> DepartmentsSchema:
        item = db.query(Department).filter(Department.id == data.id).one()
        item.name = data.name
        item.street = data.street
        item.city = data.city
        item.postcode = data.postcode
        db.commit()
        item = db.query(Department).filter(Department.id == data.id).one()
        return item

    # działa

    def add_worker(self, db: Session, department_id: int, worker_pesel: str) -> bool:
        worker = db.query(Worker).filter(
            Worker.pesel == worker_pesel).one()
        if worker:
            worker.department_id = department_id
            db.commit()
            return True
        return False

    # działa

    def delete_worker_by_id(self, db: Session, department_id: int, worker_pesel: str) -> bool:
        worker = db.query(Worker).filter(Worker.department_id ==
                                         department_id, Worker.pesel == worker_pesel).one()
        if worker:
            worker.department_id = None
            db.commit()
            return True
        return False

    def set_none_department_for_workers_in_department(self, db: Session, department_id) -> bool:
        db.query(Worker).filter(Worker.department_id == department_id).update(
            {"department_id": None}
        )
        db.commit()
        return True
