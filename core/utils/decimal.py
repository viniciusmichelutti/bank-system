from decimal import Decimal


def precision_decimal(number):
    TWOPLACES = Decimal(10) ** -2
    return Decimal(number).quantize(TWOPLACES)
