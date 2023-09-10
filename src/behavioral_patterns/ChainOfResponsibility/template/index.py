from abc import ABC as AbstractClass, abstractmethod
from dataclasses import dataclass, field
from functools import reduce
from typing import Callable, Optional


@dataclass
class User:
    username: str


@dataclass
class Request:
    path: str
    method: str


@dataclass
class Response:
    status_code: int
    body: Optional[list | dict] = None


@dataclass
class Route:
    path: str
    method: str
    handle: Callable[[Request], Response]


class MethodNotAllowed(Exception):
    pass


class NotFound(Exception):
    pass


class IAPIExceptionHandler(AbstractClass):  # Handler
    @abstractmethod
    def handle(self, exception: Exception) -> Response | None:
        pass


class NotFoundExceptionHandler(IAPIExceptionHandler):  # Concrete Handler
    def handle(self, exception: Exception) -> Response | None:
        if isinstance(exception, NotFound):
            return Response(status_code=404)
        return None


class MethodNotAllowedExceptionHandler(IAPIExceptionHandler):  # Concrete Handler
    def handle(self, exception: Exception) -> Response | None:
        if isinstance(exception, NotFound):
            return Response(status_code=405)
        return None


class Server:  # Context
    def __init__(self, routes: list[Route], exception_handlers: list[IAPIExceptionHandler]):
        self.__routes = routes
        self.__exception_handlers = exception_handlers

    def __get_route(self, request: Request) -> Route:
        for route in self.__routes:
            if route.path == request.path:
                if route.method == request.method:
                    return route
                else:
                    raise MethodNotAllowed()
        raise NotFound()

    def __get_response_from_exception_handler(self, error: Exception) -> Response | None:
        for exception_handler in self.__exception_handlers:
            response = exception_handler.handle(error)
            if response:
                return response
        return None

    def handle(self, request: Request) -> Response:
        try:
            route = self.__get_route(request)
            return route.handle(request)
        except Exception as error:
            response = self.__get_response_from_exception_handler(error)
            if response:
                return response
            return Response(status_code=500)


server = Server(
    [Route(method='GET', path='/users', handle=lambda request: Response(status_code=200, body=[]))],
    [NotFoundExceptionHandler(), MethodNotAllowedExceptionHandler()],
)

print(server.handle(Request(method='GET', path='/me')))
print(server.handle(Request(method='GET', path='/users')))
print(server.handle(Request(method='POST', path='/users')))
