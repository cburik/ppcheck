from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from ppcheck.install import create_database
from ppcheck.utils import remove_file

TMP_DB_LOC = "./tmp_database.db"


@fixture
def engine_with_empty_database():
    engine = create_engine(f"sqlite:///{TMP_DB_LOC}")
    create_database(engine)
    yield engine
    remove_file(TMP_DB_LOC)


@fixture
def session_with_empty_database(engine_with_empty_database):
    session = Session(engine_with_empty_database)
    yield session
    session.close()
