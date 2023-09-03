from abc import ABC as AbstractClass, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional


@dataclass
class BankAccount:
    created: datetime = field(init=False, default_factory=lambda: datetime.utcnow())
    name: str
    email: str
    balance: Decimal = field(init=False, default=Decimal('0.00'))
    full_credit: Decimal = field(init=False, default=Decimal('50.00'))
    invoice: Decimal = field(init=False, default=Decimal('0.00'))
    is_active: bool = field(init=False, default=True)
    last_increase_credit_request: Optional[datetime] = field(init=False, default=None)
    increase_request_in_progress: bool = field(init=False, default=False)


class IProcessPayment(AbstractClass):  # Strategy
    @abstractmethod
    def get_receiver(self, payload: dict) -> BankAccount:
        pass

    @abstractmethod
    def validate(self, sender_account: BankAccount, payload: dict) -> bool:
        pass

    @abstractmethod
    def process(self, sender_account: BankAccount, receiver_account: BankAccount, payload: dict) -> dict:
        pass
