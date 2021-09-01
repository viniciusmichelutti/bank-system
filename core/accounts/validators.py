from core.exceptions import AccountNotFound


def validate_account(account, account_number):
    if not account:
        raise AccountNotFound(account_number)
