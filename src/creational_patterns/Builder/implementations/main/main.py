from abc import ABC as AbstractClass, abstractmethod

from creational_patterns.Builder.implementations.main.module.main import JSONParser


class IJSONParserBuilder(AbstractClass):
    @abstractmethod
    def build_none(self):
        pass

    @abstractmethod
    def build_order(self):
        pass


class SystemJSONParserBuilder(IJSONParserBuilder):
    def __init__(self):
        self.__result = JSONParser()

    def build_none(self):
        self.__result.set_non_empty(False)
        self.__result.set_not_null(False)

    def build_order(self):
        self.__result.set_sort_keys(False)
        self.__result.__indent(None)

    def get_result(self) -> JSONParser:
        return self.__result


class PublicJSONParserBuilder(IJSONParserBuilder):
    def __init__(self):
        self.__result = JSONParser()

    def build_none(self):
        self.__result.set_non_empty(True)
        self.__result.set_not_null(True)

    def build_order(self):
        self.__result.set_sort_keys(True)
        self.__result.__indent(4)

    def get_result(self) -> JSONParser:
        return self.__result
