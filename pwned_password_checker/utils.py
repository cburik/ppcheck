from pathlib import Path

from sqlalchemy import Engine, create_engine

from pwned_password_checker.constants import DB_LOC


def get_engine(location: str = DB_LOC) -> Engine:
    engine = create_engine(f"sqlite:///{location}")
    yield engine
    engine.dispose()


def remove_file(location: str):
    path = Path(location)
    if path.exists():
        path.unlink()
    else:
        pass
