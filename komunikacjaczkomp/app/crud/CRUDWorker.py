from typing import List


from model.Salary import Salary
from model.Worker import Worker
from schema.Child import Child
from schema.WorkerSchema import AddWorkerSchema, WorkerSchema
from sqlalchemy import or_
from sqlalchemy.orm import Session


class CRUDWorker:

    def get_all_by_name(self, db: Session, q: str) -> List[WorkerSchema]:
        items = db.query(Worker).filter(
            or_(Worker.imie == q, Worker.nazwisko == q)).all()
        return items

    def get_all(self, db: Session) -> List[WorkerSchema]:
        items = db.query(Worker).limit(500).all()
        return items

    def get_by_pesel(self, db: Session, q: str) -> WorkerSchema:
        item = db.query(Worker).filter(Worker.pesel == q).first()
        if (item):
            return item

    def get_by_department_id(self, db: Session, department_id: int) -> List[WorkerSchema]:
        items = db.query(Worker).filter(
            Worker.department_id == department_id).all()
        return items

    def get_children(self, db: Session, worker_pesel: str) -> List[Child]:
        items = db.query(Worker.children).filter(
            Worker.pesel == worker_pesel).all()
        return items

    def delete(self, db: Session, worker_pesel: str) -> bool:
        worker_to_delete = db.query(Worker).filter(
            Worker.pesel == worker_pesel).one()
        if worker_to_delete:
            db.delete(worker_to_delete)
            db.commit()
            return True
        return False

    def add_worker(self, db: Session, data: AddWorkerSchema) -> AddWorkerSchema:
        new_worker = Worker()
        new_worker.pesel = data.pesel
        new_worker.imie = data.imie
        new_worker.nazwisko = data.nazwisko
        new_worker.age = data.age
        new_worker.criminal_record = data.criminal_record
        new_worker.department_id = data.department_id
        new_worker.children = []
        new_worker.annual_salary = 0
        db.add(new_worker)
        db.commit()
        return new_worker

    def update(self, db: Session, data: Worker) -> WorkerSchema:
        item = db.query(Worker).filter(Worker.pesel == data.pesel).one()
        item.imie = data.imie
        item.nazwisko = data.nazwisko
        item.age = data.age
        item.criminal_record = data.criminal_record
        db.commit()
        worker = db.query(Worker).filter(Worker.pesel == data.pesel).one()
        return worker

    def add_child(self, db: Session, worker_pesel: str, child: Child) -> WorkerSchema:
        worker = db.query(Worker).filter(Worker.pesel == worker_pesel).one()
        children = worker.children
        dict_child = dict(child)
        dict_child['dob'] = dict_child['dob'] + 'T00:00:00.000000'
        children.append(dict_child)
        db.query(Worker).filter(Worker.pesel == worker_pesel).update(
            {"children": children}
        )
        db.commit()
        return worker

    def add_salary(self, db: Session, worker_pesel: str, month: int, amount: int) -> WorkerSchema:
        new_salary = Salary(worker_pesel=worker_pesel,
                            month=month, amount=amount)
        db.add(new_salary)
        db.commit()
        worker = db.query(Worker).filter(Worker.pesel == worker_pesel).one()
        return worker

    def update_salary(self, db: Session, worker_pesel: str, month: int, amount: int) -> WorkerSchema:
        db.query(Salary).filter(Salary.worker_pesel == worker_pesel, Salary.month == month).update(
            {"amount": amount})
        db.commit()
        worker = db.query(Worker).filter(Worker.pesel == worker_pesel).one()
        return worker

    def delete_salaries(self, db: Session, worker_pesel: str) -> bool:
        items = db.query(Salary).filter(
            Salary.worker_pesel == worker_pesel).all()
        if items:
            db.delete(items)
            db.commit()
            return True
        return False
