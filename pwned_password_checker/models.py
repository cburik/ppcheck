import hashlib
from typing import Optional

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing_extensions import Self


class Base(DeclarativeBase):
    pass


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    account_name: Mapped[str]
    username: Mapped[Optional[str]]
    url: Mapped[Optional[str]]
    hashed_password: Mapped[str]
    row_hash: Mapped[str]

    @classmethod
    def create_account(cls, account_name: str, username: str, url: str, password: str) -> Self:
        hashed_password = cls.calculate_hash(password)
        row_hash = cls.calculate_hash(";".join([account_name, username, url]))
        return Account(
            account_name=account_name, username=username, url=url, hashed_password=hashed_password, row_hash=row_hash
        )

    @classmethod
    def calculate_hash(cls, password: str) -> str:
        sha1 = hashlib.sha1()
        sha1.update(password.encode("utf-8"))
        return sha1.hexdigest()
