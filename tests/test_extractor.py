from pwned_password_checker.extractor import CsvExtractor
from pwned_password_checker.models import Account


def test_csv_extractor_extract():
    csv_extractor = CsvExtractor("tests/resources/passwords.csv")  # TODO: make proper path thingie
    accounts = csv_extractor.extract()
    assert len(csv_extractor.accounts) == 2
    assert accounts[0].account_name == "dropbox"
    assert accounts[0].username == "user123"
    assert accounts[0].url == "dropbox.com"
    assert accounts[1].hashed_password == Account.calculate_hash("mypassword")
