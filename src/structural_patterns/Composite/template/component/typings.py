from structural_patterns.Composite.template.validators.typings import IValidator
from dataclasses import dataclass
from typing import Optional


class ValidationError(Exception):
    pass


@dataclass
class Validation:
    is_valid: bool
    raw_data: dict
    serialized_data: Optional[dict]
    json_data: Optional[str]
    errors: Optional[dict[str, str]] = None


@dataclass
class Field:
    name: str
    field_type: type
    default_value: Optional[str]
    is_required: bool
    validator: Optional[IValidator]

    def __post_init__(self):
        self.__validate()

    def __validate(self):
        if self.is_required and (self.default_value is not None):
            raise ValueError(f'The {self.name} field must not have a default value because it is a required field')


class ISerializerSettings:
    validators: dict[str, IValidator]
