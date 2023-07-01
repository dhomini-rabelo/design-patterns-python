from structural_patterns.Brigde.implementations.main.abstractor.contract import IAuthenticatorRoute
from structural_patterns.Brigde.implementations.main.implementors.contract.typings import Request, Session, User
from structural_patterns.Brigde.implementations.main.implementors.contract.main import IAuthenticator


class AuthenticatorRoute(IAuthenticatorRoute):
    def __init__(self, authenticator: IAuthenticator):
        self.__authenticator = authenticator

    def authenticate(self, request: Request, users: list[User]) -> Session:
        return self.__authenticator.get_session(request, users)
