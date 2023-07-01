from structural_patterns.Brigde.implementations.main.abstractor.service import AuthenticatorRoute
from structural_patterns.Brigde.implementations.main.implementors.contract.typings import Request, User
from structural_patterns.Brigde.implementations.main.implementors.services.basic_authenticator import (
    BasicAuthentication,
)
from structural_patterns.Brigde.implementations.main.implementors.services.microservice_authenticator import (
    MicroserviceAuthentication,
)
from structural_patterns.Brigde.implementations.main.implementors.services.token_authentiicator import (
    TokenAuthentication,
)
from decouple import config
import json


users_json_file = open(
    f'{config("BASE_PATH")}/design-patterns-python/src/structural_patterns/Brigde/implementations/main/db/users.json'
)
users = list(map(lambda user_as_dict: User(**user_as_dict), json.load(users_json_file)))
users_json_file.close()

basic_authentication = AuthenticatorRoute(BasicAuthentication())
print(basic_authentication.authenticate(Request(url='/', headers={}, body={}), users=users))
print(
    basic_authentication.authenticate(
        Request(url='/', headers={}, body={'username': 'user_1', 'password': 'password_1'}), users=users
    )
)

token_authentication = AuthenticatorRoute(TokenAuthentication())
print(token_authentication.authenticate(Request(url='/', headers={}, body={}), users=users))
print(
    token_authentication.authenticate(
        Request(url='/', headers={'Authorization': 'da6be01e-f651-4e90-8212-409062b7bbc3'}, body={}), users=users
    )
)

microservice_authentication = AuthenticatorRoute(MicroserviceAuthentication())
print(microservice_authentication.authenticate(Request(url='/', headers={}, body={}), users=users))
print(
    microservice_authentication.authenticate(
        Request(url='/', headers={'Authorization': '5d302c6b-fe2e-48f9-8dca-62670d2b3dfd'}, body={}), users=users
    )
)
