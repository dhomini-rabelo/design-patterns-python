from decimal import Decimal
from creational_patterns.AbstractFactory.implementations.main.dependencies.country_factory.contract.dependencies.financial_manager.main import (
    IFinancialManager,
)


class EUAFinancialManager(IFinancialManager):
    def get_representation(self, value: Decimal) -> str:
        return f'US$ {value:,.2f}'

    def convert_from_dollar(self, value: Decimal) -> Decimal:
        return value * Decimal('1.00')
