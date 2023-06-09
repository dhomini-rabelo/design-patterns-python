from creational_patterns.AbstractFactory.implementations.main.dependencies.country_factory.contract.dependencies.date_manager.main import (
    IDateManager,
)
from creational_patterns.AbstractFactory.implementations.main.dependencies.country_factory.contract.dependencies.financial_manager.main import (
    IFinancialManager,
)
from creational_patterns.AbstractFactory.implementations.main.dependencies.country_factory.contract.main import (
    ICountryFactory,
)
from creational_patterns.AbstractFactory.implementations.main.dependencies.country_factory.services.eua.services.date_manager.main import (
    EUADateManager,
)
from creational_patterns.AbstractFactory.implementations.main.dependencies.country_factory.services.eua.services.financial_manager.main import (
    EUAFinancialManager,
)


class EUAFactory(ICountryFactory):
    def get_financial_manager(self) -> IFinancialManager:
        return EUAFinancialManager()

    def get_date_manager(self) -> IDateManager:
        return EUADateManager()
