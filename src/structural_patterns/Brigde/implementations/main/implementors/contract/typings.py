from dataclasses import dataclass


@dataclass
class Request:
    url: str
    headers: dict
    body: dict


@dataclass
class User:
    id: int
    username: str
    password: str


@dataclass
class Session:
    user: User | None
    is_authenticated: bool
