from __future__ import annotations
from creational_patterns.Prototype.implementations.main.module.typings import IPrototype
import json


class JSONParser(IPrototype):
    def __init__(
        self,
        sort_keys: bool = False,
        non_empty: bool = False,
        not_null: bool = False,
        indent: int | None = None,
        separators: tuple[str, str] | None = None,
        ignore_keys: list[str] = [],
        convert_array_as_tuple: bool = False,
        recursive: bool = False,
    ):
        self.__sort_keys = sort_keys
        self.__non_empty = non_empty
        self.__not_null = not_null
        self.__indent = indent
        self.__separators = separators
        self.__ignore_keys = ignore_keys
        self.__convert_array_as_tuple = convert_array_as_tuple
        self.__recursive = recursive

    def set_non_empty(self, new_value: bool):
        self.__non_empty = new_value

    def set_not_null(self, new_value: bool):
        self.__not_null = new_value

    def set_indent(self, new_value: int | None):
        self.__indent = new_value

    def set_sort_keys(self, new_value: bool):
        self.__sort_keys = new_value

    def set_separators(self, new_value: tuple[str, str] | None):
        self.__separators = new_value

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
            non_empty=self.__non_empty,
            not_null=self.__not_null,
            indent=self.__indent,
            separators=self.__separators,
            ignore_keys=self.__ignore_keys,
            convert_array_as_tuple=self.__convert_array_as_tuple,
            recursive=self.__recursive,
        )
