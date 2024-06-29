from typing import List

from fastapi import Depends, FastAPI, Form, Request
from pydantic import BaseConfig
from sqlalchemy.orm import Session

from connection import SessionLocal
from crud.CRUDDepartment import CRUDDepartment
from crud.CRUDWorker import CRUDWorker
from schema.DepartmentsSchema import DepartmentsSchema
from schema.WorkerSchema import WorkerSchema, AddWorkerSchema
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from starlette.middleware.cors import CORSMiddleware


BaseConfig.arbitrary_types_allowed = True

app = FastAPI(
    title='Simple app',
    description='App for Fastapi training',
    version='0.0.0.0.1',
    terms_of_service="",
    contact={"email": "sshvets@student.wsiz.edu.pl"}
)


origins = [
    "http://localhost:8080/",
    "http://172.29.74.220:8080/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory="static"), name="static")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @app.get('/login')
# async def get_login_page():
#     return FileResponse('index.html')


# @app.post('/login')
# async def login(username: str = Form(), password: str = Form(),
#                 department: int = Form()):
#     return {"username": username, 'password': password, 'department': department}


crud = CRUDWorker()
crud_dep = CRUDDepartment()


@app.post('/api/v1/departments/add', response_model=DepartmentsSchema)
async def create_department(r: Request, db: Session = Depends(get_db)):
    dep_form = await r.json()
    department = DepartmentsSchema(**dep_form)
    new_department = crud_dep.add_department(db=db, data=department)
    return new_department


@app.get('/api/v1/departments/name/{name}', response_model=List[DepartmentsSchema])
def get_department_by_name(name: str, db: Session = Depends(get_db)):
    department = crud_dep.get_all_by_name(db=db, q=name)
    return department


@app.get('/api/v1/departments/id/{department_id}', response_model=DepartmentsSchema)
def get_department_by_id(department_id: int, db: Session = Depends(get_db)):
    department = crud_dep.get_by_id(db=db, department_id=department_id)
    return department


@app.get('/api/v1/departments/all/', response_model=List[DepartmentsSchema])
def get_all_department(db: Session = Depends(get_db)):
    departments = crud_dep.get_all(db=db)
    return departments


@app.get('/api/v1/users/name/{name}', response_model=List[WorkerSchema])
def get_user_by_name(name: str, db: Session = Depends(get_db)):
    users = crud.get_all_by_name(db=db, q=name)
    return users


@app.get('/api/v1/users/id/{pesel}', response_model=WorkerSchema)
def get_user_by_pesel(pesel: str, db: Session = Depends(get_db)):
    user = crud.get_by_pesel(db=db, q=pesel)
    return user


@app.get('/api/v1/users/department/{department_id}', response_model=List[WorkerSchema])
def get_user_by_department_id(department_id: int, db: Session = Depends((get_db))):
    users = crud.get_by_department_id(db=db, department_id=department_id)
    return users


@app.get('/api/v1/users/all', response_model=List[WorkerSchema])
def get_all_users(db: Session = Depends(get_db)):
    users = crud.get_all(db=db)
    return users


@app.post('/api/v1/users/add', response_model=AddWorkerSchema)
async def create_worker(r: Request, db: Session = Depends(get_db)):
    form = await r.json()
    worker = AddWorkerSchema(**form)
    user = crud.add_worker(db=db, data=worker)
    return user


@app.delete('/api/v1/departments/delete/{department_id}')
def delete_department_by_id(department_id: int, db: Session = Depends(get_db)):
    crud_dep.delete_department_by_id(db=db, department_id=department_id)


@app.delete('/api/v1/users/delete/{worker_pesel}')
def delete_user_by_pesel(worker_pesel: str, db: Session = Depends(get_db)):
    crud.delete(db=db, worker_pesel=worker_pesel)


@app.put('/api/v1/departments/update', response_model=DepartmentsSchema)
def update_department(department: DepartmentsSchema, db: Session = Depends(get_db)):
    department = crud_dep.update(db=db, data=department)
    return department


@app.put('/api/v1/users/update', response_model=WorkerSchema)
def update_worker(worker: WorkerSchema, db: Session = Depends(get_db)):
    worker = crud.update(db=db, data=worker)
    return worker


@app.get('/api/v1/users/children/id/{worker_pesel}')
def get_children(worker_pesel: str, r: Request, db: Session = Depends(get_db)):
    children = crud.get_children(db=db, worker_pesel=worker_pesel)
    return children


@app.put('/api/v1/users/children/add/{worker_pesel}')
async def add_children(worker_pesel: str, r: Request, db: Session = Depends(get_db)):
    child_form = await r.json()
    worker = crud.add_child(db=db, worker_pesel=worker_pesel, child=child_form)
    return worker


@app.post('/api/v1/users/salary/add/{worker_pesel}')
async def add_salary(worker_pesel: str, r: Request,  db: Session = Depends(get_db)):
    salary_form = await r.json()
    x = list(salary_form.values())
    month = x[0]
    amount = x[1]
    salary = crud.add_salary(
        db=db, worker_pesel=worker_pesel, month=month, amount=amount)
    return salary
