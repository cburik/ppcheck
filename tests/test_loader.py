from sqlalchemy import select
from sqlalchemy.orm import Session

from pwned_password_checker.loader import Loader
from pwned_password_checker.models import Account


def test_loader_load(session_with_empty_database: Session):
    session = session_with_empty_database
    loader = Loader(session)

    accounts = [
        Account.create_account("github", "user123", "https://github.com", "p@ssw0rd"),
        Account.create_account("example", "user456", "http://example.com", "password"),
    ]
    loader.load(accounts)

    statement = select(Account)
    selected_accounts = session.scalars(statement).fetchall()
    assert selected_accounts[0] == accounts[0]
    assert selected_accounts[1] == accounts[1]
