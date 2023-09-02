from abc import ABC as AbstractClass, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional


class IEmailSender(AbstractClass):
    @abstractmethod
    def send(self, to: str, message: str):
        pass


class EmailSender(IEmailSender):
    def __init__(self, host_email: str):
        self.__HOST_EMAIL = host_email

    def send(self, to: str, message: str):
        print(f'EMAIL[ {self.__HOST_EMAIL} -> {to}]: {message}')


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


class ICommand(AbstractClass):
    @abstractmethod
    def do(self, bank_account: BankAccount):
        pass

    @abstractmethod
    def undo(self, bank_account: BankAccount):
        pass


class IncreaseCreditRequestAction:  # Receiver
    def __init__(self, email_sender: IEmailSender):
        self.__email_sender = email_sender

    def request(self, bank_account: BankAccount):
        if not bank_account.is_active:
            self.__email_sender.send(
                to=bank_account.email, message='Credit increase cannot be requested on blocked accounts'
            )
        elif (not bank_account.last_increase_credit_request) or (
            bank_account.last_increase_credit_request < (datetime.utcnow() - timedelta(days=90))
        ):
            bank_account.last_increase_credit_request = datetime.utcnow()
            bank_account.increase_request_in_progress = True
            self.__email_sender.send(to=bank_account.email, message='Credit increase was requested')
        else:
            bank_account.increase_request_in_progress = False
            self.__email_sender.send(to=bank_account.email, message='Credit increase was not requested')

    def cancel(self, bank_account: BankAccount):
        if bank_account.increase_request_in_progress:
            bank_account.increase_request_in_progress = False
            self.__email_sender.send(to=bank_account.email, message='Credit increase was cancelled')


class IncreaseCreditRequestCommand(ICommand):  # Command
    def __init__(self, receiver: IncreaseCreditRequestAction):
        self.__receiver = receiver

    def do(self, bank_account: BankAccount):
        self.__receiver.request(bank_account)

    def undo(self, bank_account: BankAccount):
        self.__receiver.cancel(bank_account)


class BlockAccountCommand(ICommand):  # Command
    def do(self, bank_account: BankAccount):
        bank_account.is_active = False

    def undo(self, bank_account: BankAccount):
        bank_account.is_active = True


class BankApp:  # Invoker
    def __init__(self, commands: dict[str, ICommand]):
        self.__commands = commands

    def do_command(self, bank_account: BankAccount, command_name: str):
        self.__commands[command_name].do(bank_account)

    def undo_command(self, bank_account: BankAccount, command_name: str):
        self.__commands[command_name].undo(bank_account)


bank_app = BankApp(
    commands={
        'increase_credit': IncreaseCreditRequestCommand(
            receiver=IncreaseCreditRequestAction(email_sender=EmailSender('me@email.com.br'))
        ),
        'block_account': BlockAccountCommand(),
    }
)

bank_account = BankAccount(name='John Doe', email='john@email.com.br')

bank_app.do_command(bank_account, command_name='block_account')
bank_app.do_command(bank_account, command_name='increase_credit')
bank_app.undo_command(bank_account, 'block_account')
bank_app.do_command(bank_account, command_name='increase_credit')
bank_app.undo_command(bank_account, 'increase_credit')
