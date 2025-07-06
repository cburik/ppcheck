from sqlalchemy import Engine

from ppcheck.constants import DB_LOC
from ppcheck.engine import PpcheckEngine
from ppcheck.models import Base
from ppcheck.utils import remove_dir, remove_file


def create_database(engine: Engine):
    Base.metadata.create_all(bind=engine)


def install():
    DB_LOC.parent.mkdir(parents=True, exist_ok=True)
    engine = PpcheckEngine()
    create_database(engine)
    engine.dispose()


def uninstall():
    remove_file(DB_LOC)
    remove_dir(DB_LOC.parent)


if __name__ == "__main__":
    install()
