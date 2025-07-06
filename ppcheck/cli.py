from argparse import OPTIONAL, ArgumentParser

import pandas as pd

from ppcheck.api import ApiManager
from ppcheck.engine import PpcheckEngine
from ppcheck.extractor import CsvExtractor
from ppcheck.install import install, uninstall
from ppcheck.models import Account


class PwnedPasswordChecker:
    def __init__(self):
        self.engine = PpcheckEngine()
        self.parser = ArgumentParser(description="PwnedPasswordChecker CLI")
        self._add_arguments()

    def _add_arguments(self):
        self.parser.add_argument("--install", action="store_true", help="Run the install function")
        self.parser.add_argument("--extract", type=str, help="Extract data from the given source")
        self.parser.add_argument("--uninstall", action="store_true", help="Run the uninstall function")
        self.parser.add_argument(
            "--check",
            type=str,
            nargs=OPTIONAL,
            const="current",
            default=None,
            help="Check the database for pwned passwords. Use 'all' to check all accounts, not just current ones",
        )

    def _extract(self, path: str) -> None:
        accounts = CsvExtractor(path).extract()
        with self.engine.get_session() as session:
            Account.add_to_database(session=session, accounts=accounts)

    def _check(self, check_type) -> None:
        with self.engine.get_session() as session:
            if check_type == "all":
                accounts: pd.DataFrame = Account.get_all(session=session, as_dataframe=True)
            elif check_type == "current":
                accounts: pd.DataFrame = Account.get_all_current(session=session, as_dataframe=True)
            else:
                raise ValueError("Unexpected check type passed to --check")
        api = ApiManager()
        accounts["num_pwned"] = accounts.apply(lambda row: api.get_password_results(row.hashed_password), axis=1)
        print(accounts)

    def run(self, args=None):
        if args is None:
            args = self.parser.parse_args(args)
        # TODO: make switch statement
        if args.install:
            install()  # TODO: Add engine as an argument
        if args.uninstall:
            uninstall()
        if args.extract:
            self._extract(args.extract)
        if args.check:
            self._check(args.check)


def main():
    PwnedPasswordChecker().run()


if __name__ == "__main__":
    main()
