from datetime import datetime

from pytoniq_core import Address


class AccountSubscription:
    def __init__(self, address: Address, start_time: datetime):
        self.address = address
        self.start_time = start_time
