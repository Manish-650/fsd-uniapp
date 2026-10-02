import unittest

from uniapp.models.student import Student
from uniapp.services.credential_validator import CredentialValidator


class CredentialValidatorTests(unittest.TestCase):
    def test_valid_emails(self):
        for email in ("manish@university.com", "Manish.Kumar@university.com",
                      "student_03+lab@university.com"):
            with self.subTest(email=email):
                CredentialValidator.validate_email(email)

    def test_invalid_emails(self):
        for email in (None, 123, "", "@university.com", "a@gmail.com",
                      "a@university.com.au", "a@universityXcom", "a@@university.com",
                      ".a@university.com", "a.@university.com", "a..b@university.com",
                      "a b@university.com", " a@university.com", "a@university.com\n",
                      "a@UNIVERSITY.COM", "名字@university.com"):
            with self.subTest(email=email), self.assertRaises(ValueError):
                CredentialValidator.validate_email(email)

    def test_password_minimum_and_longer_values(self):
        for password in ("Hello123", "ABCDE123", "Example123456", "AbCdEf123"):
            CredentialValidator.validate_password(password)

    def test_invalid_passwords(self):
        for password in (None, 123, "", "Abcd123", "Abcde12", "abcde123",
                         "1Abcde123", "Abcde123x", "Abc1de123", "Abcde!123",
                         " Abcde123", "Abcde123\n", "Abcde１２３", "Ábcde123"):
            with self.subTest(password=password), self.assertRaises(ValueError):
                CredentialValidator.validate_password(password)

    def test_confirmation(self):
        CredentialValidator.validate_confirmation("Hello123", "Hello123")
        for confirmation in (None, "", "hello123", "Hello123 "):
            with self.assertRaises(ValueError):
                CredentialValidator.validate_confirmation("Hello123", confirmation)

    def test_student_creation_and_restoration_reject_invalid_credentials(self):
        for email, password in (("a@gmail.com", "Example123"),
                                ("a@university.com", "weak")):
            with self.assertRaises(ValueError):
                Student.create("Manish", email, password, set())
            with self.assertRaises(ValueError):
                Student.from_dict({"id": "000001", "name": "Manish", "email": email,
                                   "password": password, "subjects": []})

    def test_password_update_is_unchanged_on_failure(self):
        student = Student(1, "Manish", "manish@university.com", "Example123")
        for password, confirmation in (("weak", "weak"), ("Updated123", "Other123")):
            with self.assertRaises(ValueError):
                student.change_password(password, confirmation)
            self.assertEqual(student.password, "Example123")
        student.change_password("Updated123", "Updated123")
        self.assertEqual(student.password, "Updated123")


if __name__ == "__main__":
    unittest.main()
