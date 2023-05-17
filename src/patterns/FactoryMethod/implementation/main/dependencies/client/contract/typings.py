from dataclasses import dataclass


@dataclass
class APIResponse:
    status: int
    data: list[dict]
