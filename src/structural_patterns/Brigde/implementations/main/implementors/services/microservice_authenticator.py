from structural_patterns.Brigde.implementations.main.implementors.contract.main import IAuthenticator
from structural_patterns.Brigde.implementations.main.implementors.contract.typings import Request, Session, User
from decouple import config


class MicroserviceAuthentication(IAuthenticator):
    def get_session(self, request: Request, users: list[User]) -> Session:
        if request.headers.get('Authorization') == config('MICROSERVICE_ID'):
            for user in users:
                if user.id == config('MICROSERVICE_USER_ID'):
                    return Session(
                        user=user,
                        is_authenticated=True,
                    )

        return Session(
            user=None,
            is_authenticated=False,
        )
