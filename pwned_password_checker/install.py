from sqlalchemy import Engine, create_engine

from pwned_password_checker.constants import DB_LOC
from pwned_password_checker.models import Base
from pwned_password_checker.utils import remove_file


def create_database(engine: Engine):
    Base.metadata.create_all(bind=engine)


def install(location: str = DB_LOC):
    engine = create_engine(f"sqlite:///{location}")
    create_database(engine)
    engine.dispose()


def uninstall(location: str = DB_LOC):
    remove_file(location)


if __name__ == "__main__":
    install()
