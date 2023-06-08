from creational_patterns.FactoryMethod.implementations.main.dependencies.client.contract.main import IRestClient
from abc import ABC as AbstractClass, abstractmethod
from creational_patterns.FactoryMethod.implementations.main.dependencies.client.services.httpx import HttpxRestClient

from creational_patterns.FactoryMethod.implementations.main.dependencies.client.services.requests import (
    RequestsRestClient,
)


class GetTodoList(AbstractClass):
    __ROUTE = 'https://jsonplaceholder.typicode.com/todos'

    @abstractmethod
    def get_client(self) -> IRestClient:
        pass

    def get_data(self):
        client = self.get_client()
        return client.get(self.__ROUTE)


class GetTodoListWithRequests(GetTodoList):
    def get_client(self):
        return RequestsRestClient()


class GetTodoListWithHttpx(GetTodoList):
    def get_client(self):
        return HttpxRestClient()


todo_requests = GetTodoListWithRequests()
todo_httpx = GetTodoListWithHttpx()

print(todo_requests.get_data().data)
print(todo_httpx.get_data().data)
