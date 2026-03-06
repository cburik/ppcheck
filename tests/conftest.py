from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from ppcheck.encryption import EncryptionManager
from ppcheck.install import create_database
from ppcheck.settings import get_settings
from ppcheck.utils import remove_file

TMP_DB_LOC = "./tmp_database.db"


@fixture(scope="session", autouse=True)
def encryption_manager_with_test_password():
    # Set test environment variables for fast encryption in tests
    settings = get_settings()
    settings.field_iterations = 1
    settings.master_password = "testpassword"

    # Initialize manager to use test settings
    manager = EncryptionManager()
    yield manager

    # Cleanup
    manager._password = None
    manager._initialize_fernet.cache_clear()
    get_settings.cache_clear()


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
