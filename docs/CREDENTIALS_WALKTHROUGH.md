# Credential validation walkthrough

CredentialValidator is in `uniapp/services/credential_validator.py`. Keeping the rules in one place lets the future CLI and GUI use the same checks.

## How it works

Each method returns normally for valid input and raises ValueError with a readable message for invalid input.

- `validate_email(email)`: checks the whole email, including the exact @university.com domain.
- `validate_password(password)`: checks the whole password against the written assignment rule.
- `validate_confirmation(password, confirmation)`: checks that the confirmation matches exactly.

Student construction (including create and from_dict) validates credentials. A password change validates the new password and, when supplied, its confirmation before changing anything. The optional confirmation preserves existing model calls; the future user interfaces must ask for it and pass it in.

## Password pattern explained

`[A-Z][A-Za-z]{4,}[0-9]{3,}`

| Part | Meaning |
| --- | --- |
| [A-Z] | First character is an uppercase English letter |
| [A-Za-z]{4,} | At least four more letters, giving five letters in total |
| [0-9]{3,} | At least three digits after the letters |

We use re.fullmatch so extra characters, including a trailing newline, cannot slip through.

Examples: Hello123 and Example123456 pass. hello123 (lowercase start), Abcd123 (four letters), and Hello12 (two digits) fail.

The brief's sample rejects Hello123, which conflicts with its written rule. This implementation follows the written rule until the tutor clarifies it.

## Email assumption

Examples accepted: manish@university.com and manish.kumar+lab@university.com.

The local part accepts ASCII letters, digits, underscore, plus, percent and hyphen, with dots between nonempty sections. It rejects leading/trailing dots, consecutive dots, spaces, other domains and uppercase domain spelling. This is a documented working pattern because the precise local-part rule is not yet confirmed. Inputs are not silently trimmed or lowercased by the validator.

## Example

```python
from uniapp.models.student import Student

student = Student(1, "Manish", "manish@university.com", "Example123")
student.change_password("Updated123", "Updated123")

try:
    student.change_password("Another123", "Different123")
except ValueError as error:
    print(error)  # Passwords do not match.

print(student.password)  # Updated123: failed update kept the old value
```

These are format checks, not authentication. Login, duplicate-email checks and saving to students.data still need implementation. Existing dictionary records with invalid credentials will now be rejected during restoration.

Run `python -m unittest discover -s tests -v` from the repository root. All 23 tests pass, including seven new tests for credential boundaries, malformed values and Student integration.
