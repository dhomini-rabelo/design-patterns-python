from abc import ABC as AbstractClass, abstractmethod
from decimal import Decimal


class IFinancialManager(AbstractClass):
    @abstractmethod
    def get_representation(self, value: Decimal) -> str:
        pass

    @abstractmethod
    def convert_from_dollar(self, value: Decimal) -> Decimal:
        pass
