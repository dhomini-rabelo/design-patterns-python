from abc import ABC as AbstractClass, abstractmethod


class IProduct(AbstractClass):  # Component
    @abstractmethod
    def get_price(self) -> int:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass


class Product(IProduct):  # Concrete Component
    def __init__(self, name: str, value_in_cents: int):
        self.__name = name
        self.__value = value_in_cents

    def get_price(self) -> int:
        return self.__value

    def get_name(self) -> str:
        return self.__name


class IProductGetPriceDecorator(AbstractClass):  # Decorator
    @abstractmethod
    def get_price(self) -> int:
        pass


class ProductWithTaxDecorator(IProductGetPriceDecorator):  # Concrete Decorator
    def __init__(self, product: Product, tax_in_cents: int):
        self.__product = product
        self.__tax = tax_in_cents

    def get_price(self) -> int:
        return self.__product.get_price() + self.__tax


computer_without_tax = Product('Computer', 10000)
print(computer_without_tax.get_price())
computer_with_tax = ProductWithTaxDecorator(computer_without_tax, tax_in_cents=200)
print(computer_with_tax.get_price())
