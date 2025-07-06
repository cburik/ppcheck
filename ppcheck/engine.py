from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker

from ppcheck.constants import DB_LOC


class PpcheckEngine:
    _instance = None
    _engine = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PpcheckEngine, cls).__new__(cls)
            cls._engine = create_engine(f"sqlite:///{DB_LOC}")
        return cls._instance

    @property
    def engine(self) -> Engine:
        return self._engine

    def get_session(self):
        Session = sessionmaker(bind=self._engine)
        return Session()
