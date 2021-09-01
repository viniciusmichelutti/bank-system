class EventType:
    DEPOSIT = 'deposit'
    WITHDRAW = 'withdraw'
    TRANSFER = 'transfer'

    @staticmethod
    def choices():
        return [EventType.DEPOSIT, EventType.WITHDRAW, EventType.TRANSFER]
