from abc import ABC as AbstractClass, abstractmethod


class IEmailValidator(AbstractClass):
    @abstractmethod
    def validate(self, email: str) -> bool:
        pass
