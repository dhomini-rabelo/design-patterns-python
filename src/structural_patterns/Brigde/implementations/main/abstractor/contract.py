from abc import ABC as AbstractClass, abstractmethod

from structural_patterns.Brigde.implementations.main.implementors.contract.typings import Request, Session, User


class IAuthenticatorRoute(AbstractClass):
    @abstractmethod
    def authenticate(self, request: Request, users: list[User]) -> Session:
        pass
