from abc import ABC as AbstractClass, abstractmethod
from typing import Callable


IValidatorResponse = list[Callable[[str], None]]


class IValidator(AbstractClass):
    @abstractmethod
    def get_validators(self) -> IValidatorResponse:
        pass
