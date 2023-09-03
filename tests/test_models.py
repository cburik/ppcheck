from pwned_password_checker.models import Account


def test_account_calculate_hash():
    actual = Account.calculate_hash("hello")
    expected = "aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d"
    assert actual == expected


def test_account_create_account():
    account = Account.create_account("github", "user123", "https://github.com", "p@ssw0rd")
    assert account.account_name == "github"
    assert account.username == "user123"
    assert account.url == "https://github.com"

    assert account.hashed_password == Account.calculate_hash("p@ssw0rd")
    assert account.row_hash == Account.calculate_hash(f"github;user123;https://github.com")
