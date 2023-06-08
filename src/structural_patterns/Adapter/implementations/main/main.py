from structural_patterns.Adapter.implementations.main.adapter import EmailAdapterValidator
from structural_patterns.Adapter.implementations.main.target import IEmailValidator


class EmailField:
    def __init__(self, value: str, validators: list[IEmailValidator]):
        self.__value = value
        self.__validators = validators

    def is_valid(self) -> bool:
        for Validator in self.__validators:
            is_valid = Validator.validate(self.__value)
            if not is_valid:
                return False
        return True


invalid_field = EmailField('test', validators=[EmailAdapterValidator()])
print(invalid_field.is_valid())

valid_field = EmailField('test@test.com', validators=[EmailAdapterValidator()])
print(valid_field.is_valid())
