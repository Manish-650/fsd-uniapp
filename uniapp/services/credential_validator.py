"""Shared credential rules for the student model and future interfaces."""

import re


class CredentialValidator:
    # Working email assumption: common ASCII local parts, exact lowercase domain.
    EMAIL_PATTERN = r"[A-Za-z0-9_+%-]+(?:\.[A-Za-z0-9_+%-]+)*@university\.com"
    PASSWORD_PATTERN = r"[A-Z][A-Za-z]{4,}[0-9]{3,}"

    @staticmethod
    def validate_email(email):
        if (not isinstance(email, str)
                or re.fullmatch(CredentialValidator.EMAIL_PATTERN, email) is None):
            raise ValueError("Email must be a valid address ending in @university.com.")

    @staticmethod
    def validate_password(password):
        if (not isinstance(password, str)
                or re.fullmatch(CredentialValidator.PASSWORD_PATTERN, password) is None):
            raise ValueError(
                "Password must start with an uppercase letter and contain "
                "at least five letters followed by at least three digits."
            )

    @staticmethod
    def validate_confirmation(password, confirmation):
        if not isinstance(confirmation, str) or password != confirmation:
            raise ValueError("Passwords do not match.")
