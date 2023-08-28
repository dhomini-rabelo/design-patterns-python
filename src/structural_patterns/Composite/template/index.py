from abc import ABC as AbstractClass, abstractmethod
from dataclasses import dataclass, field
from decimal import Decimal
import inspect
import json
from typing import Any, Callable, Optional, Required, Self


class ValidationError(Exception):
    pass


class IValidator(AbstractClass):
    @abstractmethod
    def get_validators(self) -> list[Callable[[str], None]]:
        pass


class DefaultIntegerFieldValidator(IValidator):
    def __init__(self):
        self.__validators = [self.__get_validate_is_numeric(int)]

    def __get_validate_is_numeric(self, is_required: bool):
        def validate(value: str):
            if not value.isnumeric():
                raise ValidationError(f'Valor inválido')

        return validate

    def get_validators(self) -> list[Callable[[str], Any]]:
        return self.__validators


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


class SerializerSettings:
    validators: dict[str, IValidator] = {}


class SerializerMetaClass(type):
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        if name != 'Serializer':
            cls._fields = mcs.__get_fields(cls, cls.__annotations__.items())
        return cls

    def __get_fields(cls, fields: dict) -> list[Field]:
        def get_field(name: str, field_type: type) -> Field:
            return Field(
                name=name,
                field_type=field_type,
                default_value=getattr(cls, name) if hasattr(cls, name) else None,
                is_required=not ('typing.Optional' in str(field_type)),
                validator=(getattr(cls.Meta, 'validator').get(name) if hasattr(cls.Meta, 'validator') else None)
                if hasattr(cls, 'Meta')
                else None,
            )

        payload_fields = [get_field(name, field_type) for name, field_type in fields]

        if payload_fields == []:
            raise ValueError('Serializer without fields')

        return payload_fields


class Serializer(metaclass=SerializerMetaClass):
    _fields: list[Field]

    def __validate_required_field(self, field: Field, value: Any):
        if (value is None) and field.is_required:
            raise ValidationError('Este campo é obrigatório')

    def __get_errors(self, data: dict):
        errors = {}

        if not isinstance(data, dict):
            return {'body': 'Payload inválido'}

        for field in self._fields:
            try:
                if field.name not in data:
                    self.__validate_required_field(field, data.get(field.name))
                else:
                    for validator in [
                        *self.__get_default_validators(field),
                        *(field.validator.get_validators() if field.validator else []),
                    ]:
                        validator(data[field.name])
            except ValidationError as error:
                errors[field.name] = str(error)

        return errors

    def __get_default_validators(self, field: Field):
        if 'int' in str(field.field_type):
            return DefaultIntegerFieldValidator().get_validators()
        return []

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


class CharFieldValidator(IValidator):
    def __init__(self, max_length: Optional[int] = None):
        self.__validators = []

        if max_length:
            self.__validators.append(self.__get_validate_string_length_function(max_length))

    def __get_validate_string_length_function(self, max_length: int):
        def validate(value: str):
            if len(value) > max_length:
                raise ValidationError(f'Este campo deveria ter {max_length} caracteres')

        return validate

    def get_validators(self) -> list[Callable[[str], Any]]:
        return self.__validators


class PersonSerializer(Serializer):
    name: str
    age: Optional[int]

    class Meta(SerializerSettings):
        validator = {'name': CharFieldValidator(max_length=10)}


s = PersonSerializer()

print(s.validate({'name': 'zaerrr'}))
