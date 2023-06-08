from __future__ import annotations
from abc import ABC as AbstractClass, abstractmethod


class IPrototype(AbstractClass):
    @abstractmethod
    def clone(self) -> IPrototype:
        pass
