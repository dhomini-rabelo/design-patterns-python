from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from creational_patterns.AbstractFactory.implementations.main.dependencies.country_factory.contract.main import (
    ICountryFactory,
)
from creational_patterns.AbstractFactory.implementations.main.dependencies.country_factory.services.brazil.main import (
    BrazilFactory,
)
from creational_patterns.AbstractFactory.implementations.main.dependencies.country_factory.services.eua.main import (
    EUAFactory,
)


@dataclass
class Product:
    product_name: str
    dollar_value: Decimal


def get_transfer_report(
    buyer_country: ICountryFactory, seller_country: ICountryFactory, product: Product, utc_transfer_time: datetime
):
    buyer_date_manager = buyer_country.get_date_manager()
    buyer_financial_manager = buyer_country.get_financial_manager()
    seller_date_manager = seller_country.get_date_manager()
    seller_financial_manager = seller_country.get_financial_manager()
    return {
        'buyer': {
            'transfer_time': buyer_date_manager.get_representation(buyer_date_manager.get_datetime(utc_transfer_time)),
            'value': buyer_financial_manager.get_representation(
                buyer_financial_manager.convert_from_dollar(product.dollar_value)
            ),
        },
        'seller': {
            'transfer_time': seller_date_manager.get_representation(
                seller_date_manager.get_datetime(utc_transfer_time)
            ),
            'value': seller_financial_manager.get_representation(
                seller_financial_manager.convert_from_dollar(product.dollar_value)
            ),
        },
    }


ps5 = Product(
    product_name='PS5',
    dollar_value=Decimal('500.00'),
)


print(
    get_transfer_report(
        BrazilFactory(),
        EUAFactory(),
        ps5,
        datetime.utcnow(),
    )
)
