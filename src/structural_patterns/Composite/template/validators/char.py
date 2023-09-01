from structural_patterns.Composite.template.component.typings import ValidationError
from structural_patterns.Composite.template.validators.typings import IValidator, IValidatorResponse
from typing import Any, Callable, Optional


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

    def get_validators(self) -> IValidatorResponse:
        return self.__validators
