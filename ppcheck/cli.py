from argparse import OPTIONAL, ArgumentParser

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from ppcheck.api import ApiManager
from ppcheck.constants import DB_LOC
from ppcheck.extractor import CsvExtractor
from ppcheck.install import install, uninstall
from ppcheck.models import Account


class PwnedPasswordChecker:
    def __init__(self):
        self.engine: Engine = create_engine(f"sqlite:///{DB_LOC}")
        self.session: Session = sessionmaker(bind=self.engine)()
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
        # TODO: add column order as an argument
        # TODO: add output file as an argument

    def _extract(self, path: str) -> None:
        accounts = CsvExtractor(path).extract()
        Account.add_to_database(session=self.session, accounts=accounts)

    def _check(self, check_type) -> None:
        if check_type == "all":
            accounts = Account.get_all(session=self.session, as_dataframe=True)
        elif check_type == "current":
            accounts = Account.get_all_current(session=self.session, as_dataframe=True)
        else:
            raise ValueError("Unexpected check type passed to --check")
        api = ApiManager()
        accounts["num_pwned"] = accounts.apply(lambda row: api.get_password_results(row.hashed_password), axis=1)
        accounts = accounts[accounts["num_pwned"] > 0]
        accounts.to_csv("pwned_accounts.csv")

    def run(self, args=None):
        args = self.parser.parse_args(args)

        if args.install:
            install()  # TODO: make possible to install at different loc
        if args.extract:
            self._extract(args.extract)
        if args.check:
            self._check(args.check)
        if args.uninstall:
            uninstall()


def main():
    PwnedPasswordChecker().run()


if __name__ == "__main__":
    main()
