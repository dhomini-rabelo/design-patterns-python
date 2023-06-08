from structural_patterns.Adapter.implementations.main.adaptee import SyrusEmailValidator
from structural_patterns.Adapter.implementations.main.target import IEmailValidator


class EmailAdapterValidator(IEmailValidator):
    def __init__(self) -> None:
        self.adaptee = SyrusEmailValidator()

    def validate(self, email: str) -> bool:
        return self.adaptee.validate_email(email)
