from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker

from ppcheck.settings import get_settings


class PpcheckEngine:
    _instance = None
    _engine = None

    def __new__(cls):
        if cls._instance is None:
            settings = get_settings()
            cls._instance = super(PpcheckEngine, cls).__new__(cls)
            cls._engine = create_engine(f"sqlite:///{settings.db_loc}")
        return cls._instance

    @property
    def engine(self) -> Engine:
        return self._engine

    def get_session(self):
        Session = sessionmaker(bind=self._engine)
        return Session()
