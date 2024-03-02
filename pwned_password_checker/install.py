from pathlib import Path

from sqlalchemy import Engine, create_engine

from pwned_password_checker.constants import DB_LOC
from pwned_password_checker.models import Base
from pwned_password_checker.utils import remove_file


def create_database(engine: Engine):
    Base.metadata.create_all(bind=engine)


def install(path: Path = DB_LOC):
    path.parent.mkdir(parents=True, exist_ok=True)
    engine = create_engine(f"sqlite:///{path}")
    create_database(engine)
    engine.dispose()


def uninstall(path: Path = DB_LOC):
    remove_file(path)


if __name__ == "__main__":
    install()
