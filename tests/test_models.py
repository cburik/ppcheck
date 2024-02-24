from pwned_password_checker.models import Account


def test_account_calculate_hash():
    actual = Account.calculate_hash("hello")
    expected = "aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d"
    assert actual == expected


def test_account_create_account():
    account = Account.create_account("github", "p@ssw0rd", "user123", "https://github.com")
    assert account.account_name == "github"
    assert account.username == "user123"
    assert account.url == "https://github.com"

    hashed_password = Account.calculate_hash("p@ssw0rd")
    assert account.hashed_password == hashed_password
    assert account.record_hash == Account.calculate_hash(f"github;user123;https://github.com;{hashed_password}")


def test_account_create_account_with_nones():
    account = Account.create_account("github", "p@ssw0rd")
    assert account.account_name == "github"
    assert account.username is None
    assert account.url is None

    hashed_password = Account.calculate_hash("p@ssw0rd")
    assert account.hashed_password == hashed_password
    assert account.record_hash == Account.calculate_hash(f"github;;;{hashed_password}")


def test_account_get_all(session_with_empty_database):
    session = session_with_empty_database
    accounts = [
        Account.create_account("github", "p@ssw0rd", "user123", "https://github.com"),
        Account.create_account("example", "password", "user456", "http://example.com"),
    ]
    session.add_all(accounts)
    session.commit()

    actual = Account.get_all(session)
    assert actual == accounts


def test_account_get_all_current(session_with_empty_database):
    session = session_with_empty_database
    accounts = [
        Account.create_account("github", "p@ssw0rd", "user123", "https://github.com"),
        Account.create_account("example", "password", "user456", "http://example.com"),
    ]
    accounts[0].is_current = False
    session.add_all(accounts)
    session.commit()

    actual = Account.get_all_current(session)
    assert actual == accounts[1:]


def test_account_add_to_database(session_with_empty_database):
    session = session_with_empty_database
    accounts = [
        Account.create_account("github", "p@ssw0rd", "user123", "https://github.com"),
        Account.create_account("example", "password", "user456", "http://example.com"),
    ]
    Account.add_to_database(session, accounts)

    actual = session.query(Account).all()
    assert actual == accounts


def test_account_add_to_database_with_existing_records(session_with_empty_database):
    session = session_with_empty_database
    accounts = [
        Account.create_account("github", "p@ssw0rd", "user123", "https://github.com"),
        Account.create_account("example", "password", "user456", "http://example.com"),
    ]
    Account.add_to_database(session, accounts)

    new_accounts = [
        Account.create_account("example", "password", "user456", "http://example.com"),
        Account.create_account("new", "password", "user789", "http://new.com"),
    ]
    Account.add_to_database(session, new_accounts)
    assert session.query(Account).count() == 3
    assert session.query(Account).filter(Account.is_current).count() == 2
