from abc import ABC as AbstractClass, abstractmethod
from dataclasses import dataclass, field


@dataclass
class Product:
    id: int
    name: str
    provider: 'User'
    seller: 'User'


@dataclass
class User:
    id: int
    username: str
    email: str
    products: list[Product] = field(default_factory=list)


class IBuyProductService(AbstractClass):  # Colleague
    @abstractmethod
    def run(self, buyer: User, product: Product):
        pass


class BuyProductService(IBuyProductService):  # Concrete Colleague
    def run(self, buyer: User, product: Product):
        buyer.products.append(product)
        print(f'{buyer.username} bought a {product.name}')


class NotifyBuyService(IBuyProductService):  # Concrete Colleague
    def run(self, buyer: User, product: Product):
        print(f'Sending email to {buyer.email}')
        print(f'Sending email to {product.provider.email}')
        print(f'Sending email to {product.seller.email}')


class IBuyProductMediator(AbstractClass):  # Mediator
    @abstractmethod
    def buy(self, buyer: User, product: Product):
        pass


class BuyProductMediator(IBuyProductMediator):  # Concrete Mediator
    def __init__(self):
        self.__buy_service = BuyProductService()
        self.__notify_buy_service = NotifyBuyService()

    def buy(self, buyer: User, product: Product):
        self.__buy_service.run(buyer, product)
        self.__notify_buy_service.run(buyer, product)


user = User(id=1, username='user', email='user@email.com')

product = Product(
    id=1,
    name='Computer',
    provider=User(id=2, username='provider', email='provider@email.com'),
    seller=User(id=3, username='seller', email='seller@email.com'),
)

BuyProductMediator().buy(buyer=user, product=product)
