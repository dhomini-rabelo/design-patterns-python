from datetime import datetime, timedelta
from patterns.AbstractFactory.implementations.main.dependencies.country_factory.contract.dependencies.date_manager.main import (
    IDateManager,
)


class BrazilDateManager(IDateManager):
    def get_representation(self, datetime_obj: datetime) -> str:
        return datetime_obj.strftime('%d/%m/%Y %H:%M')

    def get_datetime(self, utc_datetime_obj: datetime) -> datetime:
        return utc_datetime_obj - timedelta(hours=3)
