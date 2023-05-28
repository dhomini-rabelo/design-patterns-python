from abc import ABC as AbstractFactory, abstractmethod
from decimal import Decimal


class IFinancialManager(AbstractFactory):
    @abstractmethod
    def get_representation(self, value: Decimal) -> str:
        pass

    @abstractmethod
    def get_today_dollar_rate(self) -> Decimal:
        pass
