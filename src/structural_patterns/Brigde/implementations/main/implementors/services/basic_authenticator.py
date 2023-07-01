from structural_patterns.Brigde.implementations.main.implementors.contract.main import IAuthenticator
from structural_patterns.Brigde.implementations.main.implementors.contract.typings import Request, Session, User
from hashlib import sha256


class BasicAuthentication(IAuthenticator):
    def get_session(self, request: Request, users: list[User]) -> Session:
        if None in [request.body.get('username'), request.body.get('password')]:
            return Session(
                user=None,
                is_authenticated=False,
            )

        for user in users:
            password_hash = sha256((request.body.get('password') or '').encode('utf-8')).hexdigest()
            if user.username == request.body.get('username') and user.password == password_hash:
                return Session(
                    user=user,
                    is_authenticated=True,
                )

        return Session(
            user=None,
            is_authenticated=False,
        )
