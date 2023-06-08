from validate_email import validate_email


class SyrusEmailValidator:
    def validate_email(self, email: str) -> bool:
        return validate_email(email)
