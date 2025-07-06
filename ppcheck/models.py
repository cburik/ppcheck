import hashlib
from datetime import datetime
from functools import lru_cache
from typing import List, Optional, Union

import pandas as pd
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column
from typing_extensions import Self


class Base(DeclarativeBase):
    created: Mapped[datetime] = mapped_column(default=datetime.now)
    updated: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    account_name: Mapped[str]
    username: Mapped[Optional[str]]
    url: Mapped[Optional[str]]
    hashed_password: Mapped[str]
    record_hash: Mapped[str]
    record_start: Mapped[datetime] = mapped_column(default=datetime.now)
    record_end: Mapped[Optional[datetime]]
    is_current: Mapped[bool] = mapped_column(default=True)

    @classmethod
    def create_account(
        cls, account_name: str, password: str, username: Optional[str] = None, url: Optional[str] = None
    ) -> Self:
        _username = username if username else ""
        _url = url if url else ""
        hashed_password = cls.calculate_hash(password)
        record_hash = cls.calculate_hash(";".join([account_name, _username, _url, hashed_password]))
        return Account(
            account_name=account_name,
            username=username,
            url=url,
            hashed_password=hashed_password,
            record_hash=record_hash,
        )  # type: ignore

    @classmethod
    @lru_cache(maxsize=128)
    def calculate_hash(cls, password: str) -> str:
        sha1 = hashlib.sha1()
        sha1.update(password.encode("utf-8"))
        return sha1.hexdigest()

    @classmethod
    def _to_dataframe(cls, accounts: List[Self]) -> pd.DataFrame:
        accounts_dict = [account.__dict__ for account in accounts]
        for account in accounts_dict:
            account.pop("_sa_instance_state", None)
        return pd.DataFrame.from_records(accounts_dict)

    @classmethod
    def get_all(cls, session: Session, as_dataframe=False) -> Union[List[Self], pd.DataFrame]:
        accounts = session.query(cls).all()
        if as_dataframe:
            return cls._to_dataframe(accounts)
        return accounts

    @classmethod
    def get_all_current(cls, session: Session, as_dataframe=False) -> Union[List[Self], pd.DataFrame]:
        accounts = session.query(cls).filter(cls.is_current).all()
        if as_dataframe:
            return cls._to_dataframe(accounts)
        return accounts

    @classmethod
    def add_to_database(cls, session: Session, accounts=List[Self]) -> None:
        new_hashes = [account.record_hash for account in accounts]
        session.query(cls).filter(cls.record_hash.not_in(new_hashes), cls.is_current).update(
            {cls.record_end: datetime.now(), cls.is_current: False}
        )
        current_records = cls.get_all_current(session)
        current_hashes = [r.record_hash for r in current_records]
        new_records = [a for a in accounts if a.record_hash not in current_hashes]
        try:
            session.add_all(new_records)
            session.commit()
        except Exception as exc:
            session.rollback()
            raise exc


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key=True)
    pwned_passwords: Mapped[int]
    check_type: Mapped[str]  # enum?
    run_date: Mapped[datetime] = mapped_column(default=datetime.now)
    is_latest: Mapped[bool] = mapped_column(default=True)

    @classmethod
    def get_latest(cls, session: Session) -> Self:
        return session.query(cls).filter(cls.is_latest).first()

    @classmethod
    def add_report(cls, session: Session, pwned_passwords: int, check_type: str) -> None:
        latest_report = cls.get_latest(session)
        if latest_report:
            latest_report.is_latest = False
        new_report = cls(pwned_passwords=pwned_passwords, check_type=check_type)
        session.add(new_report)
        session.flush()
        return new_report


class PwnedPassword(Base):
    __tablename__ = "pwned_passwords"

    id: Mapped[int] = mapped_column(primary_key=True)
    report_id: Mapped[int] = mapped_column(ForeignKey("reports.id"))
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))
