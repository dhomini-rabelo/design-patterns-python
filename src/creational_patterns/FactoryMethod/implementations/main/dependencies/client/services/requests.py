import json
from creational_patterns.FactoryMethod.implementations.main.dependencies.client.contract.main import IRestClient
from creational_patterns.FactoryMethod.implementations.main.dependencies.client.contract.typings import APIResponse
import requests


class RequestsRestClient(IRestClient):
    def get(self, route: str) -> APIResponse:
        response = requests.get(route)
        return APIResponse(
            status=response.status_code,
            data=json.loads(response.text),
        )
