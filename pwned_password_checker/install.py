from sqlalchemy import Engine

from pwned_password_checker.constants import DB_LOC
from pwned_password_checker.models import Base
from pwned_password_checker.utils import get_engine, remove_file


def create_database(engine: Engine):
    Base.metadata.create_all(bind=engine)


def install(location: str = DB_LOC):
    engine = get_engine(location)
    create_database(engine)


def uninstall(location: str = DB_LOC):
    remove_file(location)


if __name__ == "__main__":
    install()
