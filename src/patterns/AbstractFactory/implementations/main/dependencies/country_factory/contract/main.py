from abc import ABC as AbstractClass, abstractmethod
from patterns.AbstractFactory.implementations.main.dependencies.country_factory.contract.dependencies.date_manager.main import (
    IDateManager,
)
from patterns.AbstractFactory.implementations.main.dependencies.country_factory.contract.dependencies.financial_manager.main import (
    IFinancialManager,
)


class ICountryFactory(AbstractClass):
    @abstractmethod
    def get_financial_manager(self) -> IFinancialManager:
        pass

    @abstractmethod
    def get_date_manager(self) -> IDateManager:
        pass
