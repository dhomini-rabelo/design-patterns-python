from __future__ import annotations
from creational_patterns.Prototype.implementations.main.typings import IPrototype
import json


class JSONParser(IPrototype):
    def __init__(
        self,
        sort_keys: bool = False,
        indent: int | str | None = None,
        separators: tuple[str, str] | None = None,
        ignore_keys: list[str] = [],
        convert_array_as_tuple: bool = False,
        recursive: bool = False,
    ):
        self.__sort_keys = sort_keys
        self.__indent = indent
        self.__separators = separators
        self.__ignore_keys = ignore_keys
        self.__convert_array_as_tuple = convert_array_as_tuple
        self.__recursive = recursive

    def set_ignore_keys(self, new_value: list[str]):
        self.__ignore_keys = new_value

    def dumps(self, obj: dict) -> str:
        return json.dumps(
            obj,
            sort_keys=self.__sort_keys,
            indent=self.__indent,
            separators=self.__separators,
        )

    def clone(self) -> JSONParser:
        return JSONParser(
            sort_keys=self.__sort_keys,
            indent=self.__indent,
            separators=self.__separators,
            ignore_keys=self.__ignore_keys,
            convert_array_as_tuple=self.__convert_array_as_tuple,
            recursive=self.__recursive,
        )


system_json_parser = JSONParser(
    sort_keys=True,
    indent=2,
)
public_json_parser = system_json_parser.clone()
public_json_parser.set_ignore_keys(['password', 'client_secret', 'client_id', 'id'])
