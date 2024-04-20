from pathlib import Path

from conftest import TMP_DB_LOC
from sqlalchemy import Engine

from ppcheck.models import Account


def test_create_database(engine_with_empty_database: Engine):
    # Database is created in fixture
    path = Path(TMP_DB_LOC)
    assert path.exists()
    assert engine_with_empty_database.dialect.has_table(engine_with_empty_database.connect(), Account.__tablename__)
