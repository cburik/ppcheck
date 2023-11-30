from typing import List

from sqlalchemy.orm import Session

from pwned_password_checker.models import Account


class Loader:
    def __init__(self, session: Session):
        self.session = session

    def load(self, accounts: List[Account]):
        self.session.add_all(accounts)
