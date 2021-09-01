from decimal import Decimal

from accounts import account_gateway
from core.exceptions import AccountNotFound
from core.utils.decimal import precision_decimal
from events import event_gateway
from core.events.enums import EventType


def create_event(**data):
    # TODO: validate input (type, origin, destination, amount)
    event_type = data.get('type')

    create_event_by_type = {
        EventType.DEPOSIT: _deposit,
        EventType.WITHDRAW: _withdraw,
        EventType.TRANSFER: _transfer,
    }

    return create_event_by_type.get(event_type)(**data)


def _deposit(**data):
    amount = data.get('amount')
    destination_account_number = data.get('destination')

    destination_account = account_gateway.get_account_by_number(destination_account_number)
    if destination_account is None:
        destination_account = account_gateway.create_account(number=destination_account_number)

    event_gateway.create_event(type=EventType.DEPOSIT, destination_id=destination_account['id'], amount=amount)

    new_balance = precision_decimal(destination_account['balance'] + Decimal(amount))
    account_gateway.update_account(destination_account['id'], balance=new_balance)
    return {'destination': {'id': destination_account_number, 'balance': Decimal(new_balance)}}


def _withdraw(**data):
    amount = data.get('amount')
    origin_account_number = data.get('origin')

    origin_account = account_gateway.get_account_by_number(origin_account_number)
    _validate_account(origin_account, origin_account_number)

    event_gateway.create_event(type=EventType.WITHDRAW, origin_id=origin_account['id'], amount=amount)

    new_balance = precision_decimal(origin_account['balance'] - Decimal(amount))
    account_gateway.update_account(origin_account['id'], balance=new_balance)
    return {'origin': {'id': origin_account_number, 'balance': new_balance}}


def _transfer(**data):
    amount = data.get('amount')
    origin_account_number = data.get('origin')
    destination_account_number = data.get('destination')

    origin_account = account_gateway.get_account_by_number(origin_account_number)
    _validate_account(origin_account, origin_account_number)
    destination_account = account_gateway.get_account_by_number(destination_account_number)
    _validate_account(destination_account, destination_account_number)

    event_gateway.create_event(
        type=EventType.TRANSFER,
        origin_id=origin_account['id'],
        destination_id=destination_account['id'],
        amount=amount
    )

    origin_account_new_balance = precision_decimal(origin_account['balance'] - Decimal(amount))
    destination_account_new_balance = precision_decimal(destination_account['balance'] + Decimal(amount))
    account_gateway.update_account(origin_account['id'], balance=origin_account_new_balance)
    account_gateway.update_account(destination_account['id'], balance=destination_account_new_balance)

    return {
        'origin': {'id': origin_account_number, 'balance': origin_account_new_balance},
        'destination': {'id': destination_account_number, 'balance': destination_account_new_balance}
    }


def _validate_account(account, account_number):
    if not account:
        raise AccountNotFound(account_number)
