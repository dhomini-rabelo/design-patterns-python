from abc import ABC as AbstractClass, abstractmethod
from dataclasses import dataclass, field
from typing import Literal, Optional


class IVisitorValidator(AbstractClass):  # Visitor
    @abstractmethod
    def validate_field(self, value: str) -> bool:
        pass


class VisitorStringValidator(IVisitorValidator):  # Concrete Visitor
    def __init__(self, max_length=100, blank=True):
        self.__max_length = max_length
        self.__blank = blank

    def validate_field(self, value: str) -> bool:
        if len(value) > self.__max_length:
            return False
        elif (not self.__blank) and value == '':
            return False
        else:
            return True


class IFieldValidator(AbstractClass):  # Element
    _visitor: Optional[IVisitorValidator] = None

    def accept(self, visitor: IVisitorValidator):
        self._visitor = visitor


class StringValidator(IFieldValidator):  # Concrete Element
    def validate_string(self, value: str) -> bool:
        is_string = isinstance(value, str)
        if self._visitor:
            return is_string and self._visitor.validate_field(value)
        return is_string


string_validator = StringValidator()
string_validator.accept(VisitorStringValidator(max_length=10, blank=False))
print(string_validator.validate_string('2222'))
print(string_validator.validate_string('2222222222222222'))
