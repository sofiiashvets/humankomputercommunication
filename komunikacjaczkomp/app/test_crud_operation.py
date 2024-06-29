import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.crud.CRUDDepartment import CRUDDepartment
from app.crud.CRUDWorker import CRUDWorker
from app.schema.DepartmentsSchema import DepartmentsSchema
from app.schema.WorkerSchema import WorkerSchema
from connection import Session


# Set up the test database
engine = create_engine('postgresql+psycopg2://postgres:password@localhost:5432/database10', echo=False, pool_size=50, max_overflow=100)
Base = declarative_base()

# Create session
Session = sessionmaker(autocommit=False, autoflush=True, bind=engine)

# Initialize the CRUD classes
crud_workers = CRUDWorker()
crud_department = CRUDDepartment()

@pytest.fixture(scope="module")
def db():
    """Create a new database session for a test."""
    db = Session()
    try:
        yield db
    finally:
        db.close()

def test_create_worker(db):
    worker_data = WorkerSchema(
        pesel="99092012921",
        imie="John",
        nazwisko="Doe",
        age=30,
        criminal_record=False,
        children=[],
        department_id=20
    )
    created_worker = crud_workers.add_or_update(db, worker_data)
    assert created_worker.pesel == worker_data.pesel
    assert created_worker.imie == worker_data.imie
    assert created_worker.nazwisko == worker_data.nazwisko

def test_get_worker(db):
    worker = crud_workers.get(db, 99092012921)
    assert worker is not None
    assert worker.pesel == "99092012921"

def test_update_worker(db):
    worker_data = WorkerSchema(
        pesel="99092012921",
        imie="Jane",
        nazwisko="Doeve",
        age=32,
        criminal_record=False,
        children=[{},{}],
        department_id=20
    )
    updated_worker = crud_workers.add_or_update(db, worker_data)
    assert updated_worker.imie == "Jane"
    assert updated_worker.age == 32

def test_delete_worker(db):
    result = crud_workers.delete(db, "99092012921")
    assert result is True
    worker = crud_workers.get(db, 99092012921)
    assert worker is None

def test_create_department(db):
    department_data = DepartmentsSchema(
        id=1,
        name="HR",
        street="Main St",
        city="Anytown",
        postcode="12-345"
    )
    created_department = crud_department.add_or_update(db, department_data)
    assert created_department.id == department_data.id
    assert created_department.name == department_data.name

def test_get_department(db):
    department = crud_department.get(db, 1)
    assert department is not None
    assert department.name == "HR"

def test_update_department(db):
    department_data = DepartmentsSchema(
        id=1,
        name="Human Resources",
        street="Main St",
        city="Anytown",
        postcode="12-345"
    )
    updated_department = crud_department.add_or_update(db, department_data)
    assert updated_department.name == "Human Resources"
