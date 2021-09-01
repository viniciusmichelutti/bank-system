from accounts import account_gateway
from core.accounts.validators import validate_account


def get_balance(account_number):
    account = account_gateway.get_account_by_number(account_number)
    validate_account(account, account_number)

    return account['balance']
