class EntityNotFound(Exception):
    pass


class AccountNotFound(EntityNotFound):
    def __init__(self, account_number):
        message = f'Account {account_number} not found.'
        super(AccountNotFound, self).__init__(message)
