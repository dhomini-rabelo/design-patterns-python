from structural_patterns.Adapter.implementations.with_inheritance.adaptee import SyrusEmailValidator
from structural_patterns.Adapter.implementations.with_inheritance.target import IEmailValidator


class EmailAdapterValidator(IEmailValidator, SyrusEmailValidator):
    def validate(self, email: str) -> bool:
        return self.validate_email(email)
