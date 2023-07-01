import json
from structural_patterns.Brigde.implementations.main.implementors.contract.main import IAuthenticator
from structural_patterns.Brigde.implementations.main.implementors.contract.typings import Request, Session, User
from decouple import config


class TokenAuthentication(IAuthenticator):
    def __init__(self):
        tokens_json_file = open(
            f'{config("BASE_PATH")}/design-patterns-python/src/structural_patterns/Brigde/implementations/main/db/tokens.json'
        )
        self.__tokens: dict[str, str] = json.load(tokens_json_file)
        tokens_json_file.close()

    def get_session(self, request: Request, users: list[User]) -> Session:
        if request.headers.get('Authorization') in self.__tokens.keys():
            authenticated_user_id = self.__tokens[request.headers['Authorization']]
            for user in users:
                if user.id == authenticated_user_id:
                    return Session(
                        user=user,
                        is_authenticated=True,
                    )

        return Session(
            user=None,
            is_authenticated=False,
        )
