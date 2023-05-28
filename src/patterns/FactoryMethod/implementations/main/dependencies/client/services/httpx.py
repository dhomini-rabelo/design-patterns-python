import json
from patterns.FactoryMethod.implementations.main.dependencies.client.contract.main import IRestClient
from patterns.FactoryMethod.implementations.main.dependencies.client.contract.typings import APIResponse
import httpx


class HttpxRestClient(IRestClient):
    def get(self, route: str) -> APIResponse:
        response = httpx.get(route)
        return APIResponse(
            status=response.status_code,
            data=response.json(),
        )
