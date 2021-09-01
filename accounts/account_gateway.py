from core.utils.database import model_as_dict


def create_account(**attributes):
    from accounts.models import Account

    created_account = Account.objects.create(**attributes)
    return model_as_dict(created_account)


def get_account_by_number(account_number):
    from accounts.models import Account

    try:
        account_found = model_as_dict(Account.objects.get(number=account_number))
    except Account.DoesNotExist:
        account_found = None

    return account_found
