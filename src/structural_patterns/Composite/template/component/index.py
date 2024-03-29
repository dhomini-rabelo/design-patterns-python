from structural_patterns.Composite.template.component.errors import ValidationError
from structural_patterns.Composite.template.component.typings import Field, Validation
import json
from typing import Any


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


class Serializer(metaclass=SerializerMetaClass):  # Component
    _fields: list[Field]

    def __validate_required_field(self, field: Field, value: Any):
        if (value is None) and field.is_required:
            raise ValidationError('Este campo é obrigatório')

    def __get_errors(self, data: dict):
        errors = {}
        name_of_the_fields = [field.name for field in self._fields]

        for field_name in data.keys():
            if field_name not in name_of_the_fields:
                return {'body': f'{field_name} é um campo inexistente'}

        if not isinstance(data, dict):
            return {'body': 'Payload inválido'}

        for field in self._fields:
            try:
                if field.name not in data:
                    self.__validate_required_field(field, data.get(field.name))
                elif isinstance(field.field_type, type) and issubclass(field.field_type, Serializer):
                    validation = field.field_type().validate(data[field.name])
                    if not validation.is_valid:
                        raise ValidationError(validation.errors)  # Call Leaf
                else:
                    for validator in [
                        *(field.default_validator.get_validators() if field.default_validator else []),
                        *(field.validator.get_validators() if field.validator else []),
                    ]:
                        validator(data[field.name])
            except ValidationError as error:
                errors[field.name] = error.args[0]

        return errors

    def validate(self, data: dict) -> Validation:
        errors = self.__get_errors(data)

        if errors:
            return Validation(is_valid=False, raw_data=data, serialized_data=None, json_data=None, errors=errors)

        complete_data = self.__get_complete_data(data)

        return Validation(
            is_valid=True,
            raw_data=complete_data,
            serialized_data=self.to_serialized_data(complete_data),
            json_data=self.to_json(complete_data),
        )

    def __get_complete_data(self, data: dict) -> dict:
        return {field.name: (data.get(field.name) or field.default_value) for field in self._fields}

    def to_json(self, complete_data: dict[str, str]) -> str:
        return json.dumps(complete_data)

    def to_serialized_data(self, complete_data: dict) -> dict:
        def get_serialize_field(field: Field, field_value: Any):
            if field_value is None:
                return field.default_value
            elif 'int' in str(field.field_type):
                return int(field_value)
            elif isinstance(field.field_type, type) and issubclass(field.field_type, Serializer):
                return field.field_type().to_serialized_data(field_value)  # Call Leaf
            return field_value

        return {field.name: (get_serialize_field(field, complete_data.get(field.name))) for field in self._fields}
