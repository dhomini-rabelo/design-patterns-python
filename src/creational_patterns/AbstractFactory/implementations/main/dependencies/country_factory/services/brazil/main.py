from creational_patterns.AbstractFactory.implementations.main.dependencies.country_factory.contract.dependencies.date_manager.main import (
    IDateManager,
)
from creational_patterns.AbstractFactory.implementations.main.dependencies.country_factory.contract.dependencies.financial_manager.main import (
    IFinancialManager,
)
from creational_patterns.AbstractFactory.implementations.main.dependencies.country_factory.contract.main import (
    ICountryFactory,
)
from creational_patterns.AbstractFactory.implementations.main.dependencies.country_factory.services.brazil.services.date_manager.main import (
    BrazilDateManager,
)
from creational_patterns.AbstractFactory.implementations.main.dependencies.country_factory.services.brazil.services.financial_manager.main import (
    BrazilFinancialManager,
)


class BrazilFactory(ICountryFactory):
    def get_financial_manager(self) -> IFinancialManager:
        return BrazilFinancialManager()

    def get_date_manager(self) -> IDateManager:
        return BrazilDateManager()
