from abc import ABC as AbstractClass, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Literal, Optional, TypedDict


@dataclass
class ValidationResponse:
    is_valid: bool
    errors: Optional[dict] = None


@dataclass
class ProcessResponse:
    created: datetime = field(init=False, default_factory=lambda: datetime.utcnow())
    sender: str
    receiver: str
    value: Decimal
    payment_method: Literal['PIX', 'CREDIT_CARD', 'DEBIT_CARD']
    extra: dict


@dataclass
class BankAccount:
    name: str
    email: str
    balance: Decimal = field(init=False, default=Decimal('100.00'))
    full_credit: Decimal = field(init=False, default=Decimal('50.00'))
    invoice: Decimal = field(init=False, default=Decimal('0.00'))
    is_active: bool = field(init=False, default=True)
    last_increase_credit_request: Optional[datetime] = field(init=False, default=None)
    increase_request_in_progress: bool = field(init=False, default=False)


class IPayload(TypedDict):
    receiver: str
    value: Decimal


class IProcessPayment(AbstractClass):  # Strategy
    @abstractmethod
    def get_receiver(self, payload: IPayload) -> BankAccount:
        pass

    @abstractmethod
    def validate(self, sender_account: BankAccount, payload: IPayload) -> ValidationResponse:
        pass

    @abstractmethod
    def process(self, sender_account: BankAccount, receiver_account: BankAccount, payload: IPayload) -> ProcessResponse:
        pass


class ProcessPIXPayment(IProcessPayment):  # Concrete Strategy
    def get_receiver(self, payload: IPayload) -> BankAccount:
        receiver_key = payload['receiver']
        if receiver_key == 'any@email.com':
            return BankAccount('any', 'any@email.com')
        else:
            raise ValueError(f'{payload["receiver"]} key not found')

    def validate(self, sender_account: BankAccount, payload: IPayload) -> ValidationResponse:
        if sender_account.balance >= payload['value']:
            return ValidationResponse(
                is_valid=True,
            )
        else:
            return ValidationResponse(is_valid=False, errors={'sender_account': 'Value greater than balance'})

    def process(self, sender_account: BankAccount, receiver_account: BankAccount, payload: IPayload) -> ProcessResponse:
        sender_account.balance -= payload['value']
        receiver_account.balance += payload['value']
        return ProcessResponse(
            sender=sender_account.name,
            receiver=receiver_account.name,
            payment_method='PIX',
            value=payload['value'],
            extra={
                'key': payload['receiver'],
            },
        )
