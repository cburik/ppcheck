from sqlalchemy import Engine

from ppcheck.engine import PpcheckEngine
from ppcheck.models import Base
from ppcheck.settings import get_settings
from ppcheck.utils import remove_dir, remove_file


def create_database(engine: Engine):
    Base.metadata.create_all(bind=engine)


def install():
    settings = get_settings()
    settings.app_home.mkdir(parents=True, exist_ok=True)
    ppcheck_engine = PpcheckEngine()
    create_database(ppcheck_engine.engine)


def uninstall():
    settings = get_settings()
    remove_file(settings.db_loc)
    remove_dir(settings.app_home)


if __name__ == "__main__":
    install()
