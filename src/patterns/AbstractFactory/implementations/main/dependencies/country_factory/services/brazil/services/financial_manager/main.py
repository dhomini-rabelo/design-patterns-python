from decimal import Decimal
from patterns.AbstractFactory.implementations.main.dependencies.country_factory.contract.dependencies.financial_manager.main import (
    IFinancialManager,
)


class BrazilFinancialManager(IFinancialManager):
    def get_representation(self, value: Decimal) -> str:
        return f'{value:,.2f}'.replace('.', '-').replace(',', '.').replace('-', ',')

    def convert_from_dollar(self, value: Decimal) -> Decimal:
        return value * Decimal('5.00')
