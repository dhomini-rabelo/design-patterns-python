from abc import ABC as AbstractClass, abstractmethod

from structural_patterns.Brigde.implementations.main.implementors.contract.typings import Request, Session, User


class IAuthenticator(AbstractClass):
    @abstractmethod
    def get_session(self, request: Request, users: list[User]) -> Session:
        pass
