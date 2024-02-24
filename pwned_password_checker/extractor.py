from typing import List, Optional

import pandas as pd

from pwned_password_checker.models import Account


class CsvExtractor:
    def __init__(
        self,
        path: str,
        column_order: List[str] = ["account_name", "username", "url", "password"],
    ):
        self.csv_path: str = path
        self.column_order: List[str] = column_order
        self.accounts: Optional[List[Account]] = None

    def extract(self) -> List[Account]:
        passwords_dataframe: pd.DataFrame = pd.read_csv(self.csv_path, header=0, names=self.column_order)
        self.accounts = [
            Account.create_account(
                account_name=row.account_name,
                password=row.password,
                username=row.username,
                url=row.url,
            )  # type: ignore
            for row in passwords_dataframe.itertuples()
        ]
        return self.accounts
