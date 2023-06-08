from abc import ABC as AbstractClass, abstractmethod
from datetime import datetime


class IDateManager(AbstractClass):
    @abstractmethod
    def get_representation(self, datetime_obj: datetime) -> str:
        pass

    @abstractmethod
    def get_datetime(self, utc_datetime_obj: datetime) -> datetime:
        pass
