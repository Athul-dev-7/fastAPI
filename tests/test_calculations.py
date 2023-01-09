import pytest
from app.calculations import add, BankAccount, InsufficientFunds


@pytest.mark.parametrize(
    "num1,num2,expected",
    [
        (3, 2, 5),
        (1, 2, 3),
        (3, 3, 6),
        (3, 7, 10),
        (4, 3, 7),
    ],
)
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected


@pytest.fixture
def zero_bank_account():
    return BankAccount()


@pytest.fixture
def bank_account():
    return BankAccount(50)


def test_bank_set_initial_balance(bank_account):
    assert bank_account.balance == 50


def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0


def test_withdraw(bank_account):
    bank_account.withdraw(30)
    assert bank_account.balance == 20


def test_deposit(bank_account):
    bank_account.deposit(30)
    assert bank_account.balance == 80


def test_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance) == 55


@pytest.mark.parametrize(
    "deposited,withdraw,expected",
    [
        (500, 200, 300),
        (200, 200, 0),
        (300, 200, 100),
    ],
)
def test_bank_transaction(zero_bank_account, deposited, withdraw, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.balance == expected


def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(100)
