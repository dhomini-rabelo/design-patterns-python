from typing import TypedDict


class IUser(TypedDict):
    id: int
    username: str


class IData(TypedDict):
    users: list[IUser]
