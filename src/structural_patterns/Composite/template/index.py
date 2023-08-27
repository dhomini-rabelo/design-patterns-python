from abc import ABC as AbstractClass, abstractmethod
from dataclasses import dataclass, field
from decimal import Decimal
import inspect
import json
from typing import Any, Callable, Optional, Required, Self


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
    validators: list[Callable[[str], str]] = field(default_factory=list)

    def __post_init__(self):
        self.__validate()

    def __validate(self):
        if self.is_required and (self.default_value is not None):
            raise ValueError(f'The {self.name} field must not have a default value because it is a required field')


@dataclass
class CharField(Field):
    validators: list[Callable[[str], str]] = field(default_factory=lambda: [CharField.validate_field_type])

    @staticmethod
    def validate_field_type(value: str):
        if not isinstance(value, str):
            raise ValidationError(f'Este campo não representa um texto válido')
        return value


class ISerializer(AbstractClass):
    @abstractmethod
    def validate(self, data: dict) -> Validation:
        pass

    @abstractmethod
    def to_json(self, data: dict) -> str:
        pass

    @abstractmethod
    def to_serialized_data(self, data: dict) -> dict:
        pass


class Serializer(ISerializer):
    name: str
    age: Optional[int] = 1

    def __init__(self) -> None:
        self.__fields = self.__get_fields()

    def __get_fields(self) -> list[Field]:
        def get_field(name: str, field_type: type) -> Field:
            FieldClass = CharField if field_type == str else Field
            return FieldClass(
                name=name,
                field_type=field_type,
                default_value=getattr(self, name) if hasattr(self, name) else None,
                is_required=not ('typing.Optional' in str(field_type)),
            )

        return [get_field(name, field_type) for name, field_type in self.__annotations__.items()]

    def __validate_required_field(self, field: Field, value: Any):
        if (value is None) and field.is_required:
            raise ValidationError('Este campo é obrigatório')

    def __get_errors(self, data: dict):
        errors = {}

        if not isinstance(data, dict):
            return {'body': 'Payload inválido'}

        for field in self.__fields:
            try:
                if field.name not in data:
                    self.__validate_required_field(field, data.get(field.name))
                else:
                    for validator in field.validators:
                        validator(data[field.name])
            except ValidationError as error:
                errors[field.name] = str(error)

        return errors

    def validate(self, data: dict) -> Validation:
        errors = self.__get_errors(data)

        if errors:
            return Validation(is_valid=False, raw_data=data, serialized_data=None, json_data=None, errors=errors)

        return Validation(
            is_valid=True,
            raw_data=data,
            serialized_data=self.to_serialized_data(data),
            json_data=self.to_json(data),
        )

    def to_json(self, data: dict[str, str]) -> str:
        return json.dumps(data)

    def to_serialized_data(self, data: dict) -> dict:
        return data


s = Serializer()
print(
    s.validate(
        {
            'age': '25',
        }
    )
)
