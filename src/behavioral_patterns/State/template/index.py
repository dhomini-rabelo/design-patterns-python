from abc import ABC as AbstractClass, abstractmethod
from dataclasses import dataclass, field


@dataclass
class Channel:
    id: int
    name: str
    owner: 'User'


class IAccountLevelState(AbstractClass):  # State
    @abstractmethod
    def subscribe(self, channel: Channel):
        pass

    @abstractmethod
    def notify_payment(self):
        pass


class FreeAccountLevel(IAccountLevelState):  # Concrete State
    def subscribe(self, channel: Channel):
        print(f'Thank you for subscribing on {channel.name}')

    def notify_payment(self):
        print('Subscribe to paid account')


class PremiumAccountLevel(IAccountLevelState):  # Concrete State
    def subscribe(self, channel: Channel):
        print(f'Sending email to {channel.owner.email}')

    def notify_payment(self):
        print('pay 10 dollars')


@dataclass
class User:  # Context
    id: int
    username: str
    email: str
    subscriptions: list[Channel]
    account_level_state: IAccountLevelState = field(default_factory=FreeAccountLevel)

    def subscribe(self, channel: Channel):
        self.subscriptions.append(channel)
        self.account_level_state.subscribe(channel)

    def pay_for_premium_account(self):
        self.account_level_state = PremiumAccountLevel()

    def notify_payment(self):
        self.account_level_state.notify_payment()


channel_1 = Channel(
    id=1, name='Channel 1', owner=User(id=1, username='owner', email='owner@email.com', subscriptions=[])
)

user_with_free_account = User(id=2, username='user', email='user@email.com', subscriptions=[])
user_with_free_account.subscribe(channel_1)
user_with_free_account.notify_payment()

user_with_premium_account = User(id=3, username='user3', email='user3@email.com', subscriptions=[])
user_with_premium_account.pay_for_premium_account()
user_with_premium_account.subscribe(channel_1)
user_with_premium_account.notify_payment()
