from abc import ABC as AbstractClass, abstractmethod
from typing import Callable


class IValidator(AbstractClass):
    @abstractmethod
    def get_validators(self) -> list[Callable[[str], None]]:
        pass
