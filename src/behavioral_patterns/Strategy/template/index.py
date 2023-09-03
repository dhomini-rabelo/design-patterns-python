from abc import ABC as AbstractClass, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Literal, NotRequired, Optional, TypedDict


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
    extra: Optional[dict] = None


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
    password: NotRequired[str]


class IProcessPayment(AbstractClass):  # Strategy
    @abstractmethod
    def get_receiver(self, payload: IPayload) -> BankAccount:
        pass

    @abstractmethod
    def can_transfer(self, sender_account: BankAccount, payload: IPayload) -> ValidationResponse:
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

    def can_transfer(self, sender_account: BankAccount, payload: IPayload) -> ValidationResponse:
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


class ProcessDebitCardPayment(IProcessPayment):  # Concrete Strategy
    def get_receiver(self, payload: IPayload) -> BankAccount:
        receiver_id = payload['receiver']
        if receiver_id == '238238238932892392893':
            return BankAccount('any', 'any@email.com')
        else:
            raise ValueError(f'{payload["receiver"]} id not found')

    def can_transfer(self, sender_account: BankAccount, payload: IPayload) -> ValidationResponse:
        password = payload.get('password')
        if not password:
            return ValidationResponse(is_valid=False, errors={'password': 'This field is required'})
        elif password != '1234':
            return ValidationResponse(is_valid=False, errors={'password': 'Invalid password'})
        elif payload['value'] > sender_account.balance:
            return ValidationResponse(is_valid=False, errors={'sender_account': 'Value greater than balance'})
        else:
            return ValidationResponse(
                is_valid=True,
            )

    def process(self, sender_account: BankAccount, receiver_account: BankAccount, payload: IPayload) -> ProcessResponse:
        sender_account.balance -= payload['value']
        receiver_account.balance += payload['value']
        return ProcessResponse(
            sender=sender_account.name,
            receiver=receiver_account.name,
            payment_method='DEBIT_CARD',
            value=payload['value'],
            extra={},
        )


class ProcessCreditCardPayment(IProcessPayment):  # Concrete Strategy
    def get_receiver(self, payload: IPayload) -> BankAccount:
        receiver_id = payload['receiver']
        if receiver_id == '238238238932892392893':
            return BankAccount('any', 'any@email.com')
        else:
            raise ValueError(f'{payload["receiver"]} id not found')

    def can_transfer(self, sender_account: BankAccount, payload: IPayload) -> ValidationResponse:
        password = payload.get('password')
        if not password:
            return ValidationResponse(is_valid=False, errors={'password': 'This field is required'})
        elif password != '1234':
            return ValidationResponse(is_valid=False, errors={'password': 'Invalid password'})
        elif payload['value'] > sender_account.full_credit:
            return ValidationResponse(is_valid=False, errors={'sender_account': 'Value greater than full credit'})
        else:
            return ValidationResponse(
                is_valid=True,
            )

    def process(self, sender_account: BankAccount, receiver_account: BankAccount, payload: IPayload) -> ProcessResponse:
        sender_account.full_credit -= payload['value']
        receiver_account.balance += payload['value']
        return ProcessResponse(
            sender=sender_account.name,
            receiver=receiver_account.name,
            payment_method='CREDIT_CARD',
            value=payload['value'],
            extra={},
        )


class ProcessPaymentService:  # Context
    def run(self, sender_account: BankAccount, process_payment: IProcessPayment, payload: IPayload) -> ProcessResponse:
        receiver_account = process_payment.get_receiver(payload)
        can_transfer = process_payment.can_transfer(sender_account, payload)
        if can_transfer.is_valid:
            return process_payment.process(sender_account, receiver_account, payload)
        else:
            raise ValueError(can_transfer.errors)


process_payment_service = ProcessPaymentService()
bank_account = BankAccount('John Doe', 'john@email.com')

print(
    process_payment_service.run(
        sender_account=bank_account,
        process_payment=ProcessPIXPayment(),
        payload={'receiver': 'any@email.com', 'value': Decimal('50')},
    )
)

print(
    process_payment_service.run(
        sender_account=bank_account,
        process_payment=ProcessDebitCardPayment(),
        payload={'receiver': '238238238932892392893', 'value': Decimal('50'), 'password': '1234'},
    )
)

print(
    process_payment_service.run(
        sender_account=bank_account,
        process_payment=ProcessCreditCardPayment(),
        payload={'receiver': '238238238932892392893', 'value': Decimal('50'), 'password': '1234'},
    )
)


print(bank_account)
