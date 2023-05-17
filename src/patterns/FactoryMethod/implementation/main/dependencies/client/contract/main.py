from patterns.FactoryMethod.implementation.main.dependencies.client.contract.typings import APIResponse
from abc import ABC as AbstractClass, abstractmethod


class IRestClient(AbstractClass):
    @abstractmethod
    def get(self, route: str) -> APIResponse:
        pass
