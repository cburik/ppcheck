from argparse import OPTIONAL, ArgumentParser

import pandas as pd
from sqlalchemy import select

from ppcheck.api import ApiManager
from ppcheck.engine import PpcheckEngine
from ppcheck.extractor import CsvExtractor
from ppcheck.install import install, uninstall
from ppcheck.models import Account, PwnedPassword, Report


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
        self.parser.add_argument(
            "--report",
            action="store_true",
            help="Generate a report of the latest pwned passwords found in the database",
        )

    def _extract(self, path: str) -> None:
        accounts = CsvExtractor(path).extract()
        with self.engine.get_session() as session:
            Account.add_to_database(session=session, accounts=accounts)

    def _check(self, check_type) -> None:
        print(f"Checking for pwned passwords in {check_type} accounts...")
        with self.engine.get_session() as session:
            if check_type == "all":
                accounts: pd.DataFrame = Account.get_all(session=session, as_dataframe=True)
            elif check_type == "current":
                accounts: pd.DataFrame = Account.get_all_current(session=session, as_dataframe=True)
            else:
                raise ValueError("Unexpected check type passed to --check")
        api = ApiManager()
        print(f"Checking {accounts.shape[0]} accounts for pwned passwords...")
        accounts["pwned_count"] = accounts.apply(lambda row: api.get_password_results(row.hashed_password), axis=1)
        with PpcheckEngine().get_session() as session:
            pwned_passwords = accounts[accounts["pwned_count"] > 0]
            if not pwned_passwords.empty:
                report = Report.add_report(
                    session=session, pwned_passwords=pwned_passwords.shape[0], check_type=check_type
                )
                for _, row in pwned_passwords.iterrows():
                    pwned_password = PwnedPassword(
                        report_id=report.id, account_id=row["id"], pwned_count=row["pwned_count"]
                    )
                    session.add(pwned_password)
                session.commit()

    def _report(self) -> None:
        with self.engine.get_session() as session:
            latest_report = Report.get_latest(session=session)
            if latest_report:
                select_stmt = (
                    select(Account.account_name, Account.username, Account.url, PwnedPassword.pwned_count)
                    .select_from(PwnedPassword)
                    .where(PwnedPassword.report_id == latest_report.id)
                    .join(Account, PwnedPassword.account_id == Account.id)
                )
                pwned_passwords = pd.read_sql(select_stmt, session.bind)
                if pwned_passwords.empty:
                    print("No pwned passwords found in the latest report.")
                    return

                max_account_name_length = pwned_passwords["account_name"].str.len().max() + 2  # Adding 2 for padding
                max_username_length = pwned_passwords["username"].str.len().max() + 2  # Adding 2 for padding

                print("\n=== Latest Report ===")
                print(f"Date: {latest_report.run_date}")
                print(f"Pwned Passwords Found: {latest_report.pwned_passwords}")
                print(f"Check Type: {latest_report.check_type}")
                print("\n")
                print("Pwned Accounts:")
                print("-" * 70)
                print(
                    f"{'Account':<{max_account_name_length}} {'Username':<{max_username_length}} {'Pwned Count':<12} {'URL'}"  # noqa: E501
                )
                print("-" * 70)
                for _, row in pwned_passwords.iterrows():
                    print(
                        f"{row['account_name']:<{max_account_name_length}} {str(row['username']):<{max_username_length}} {str(row['pwned_count']):<12} {row['url']}"  # noqa: E501
                    )
                print("-" * 70)
            else:
                print("No reports found.")

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
        if args.report or args.check:
            self._report()


def main():
    PwnedPasswordChecker().run()


if __name__ == "__main__":
    main()
