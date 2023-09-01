from structural_patterns.Composite.template.component.errors import ValidationError
from structural_patterns.Composite.template.validators.typings import IValidator, IValidatorResponse


class DefaultIntegerFieldValidator(IValidator):
    def __init__(self):
        self.__validators = [self.__get_validate_is_numeric()]

    def __get_validate_is_numeric(self):
        def validate(value: str):
            if not value.isnumeric():
                raise ValidationError(f'Valor inválido')

        return validate

    def get_validators(self) -> IValidatorResponse:
        return self.__validators
