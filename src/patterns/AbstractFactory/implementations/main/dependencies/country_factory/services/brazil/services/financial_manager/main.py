from decimal import Decimal
from patterns.AbstractFactory.implementations.main.dependencies.country_factory.contract.dependencies.financial_manager.main import (
    IFinancialManager,
)


class BrazilFinancialManager(IFinancialManager):
    def get_representation(self, value: Decimal) -> str:
        return f'{value:,.2f}'.replace('.', '-').replace(',', '.').replace('-', ',')

    def get_today_dollar_rate(self) -> Decimal:
        return Decimal('0.20')
