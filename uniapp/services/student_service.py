"""Student workflows shared by the terminal and future GUI."""

from uniapp.models.student import Student
from uniapp.services.credential_validator import CredentialValidator


class StudentService:
    def __init__(self, database):
        self.database = database

    def register(self, name, email, password):
        CredentialValidator.validate_email(email)
        CredentialValidator.validate_password(password)
        students = self.database.get_all()
        if any(student.email == email for student in students):
            raise ValueError("Email is already registered.")
        student = Student.create(name, email, password, {s.id for s in students})
        self.database.add(student)
        return student

    def login(self, email, password):
        CredentialValidator.validate_email(email)
        CredentialValidator.validate_password(password)
        student = self.database.find_by_email(email)
        if student is None or student.password != password:
            raise ValueError("Incorrect email or password.")
        return student

    def get_student(self, student_id):
        return self.database.get_by_id(student_id)

    def enrol(self, student_id):
        student = self.get_student(student_id)
        subject = student.enrol()
        self.database.update(student)
        return subject

    def remove_subject(self, student_id, subject_id):
        student = self.get_student(student_id)
        student.remove_subject(subject_id)
        self.database.update(student)

    def change_password(self, student_id, password, confirmation):
        CredentialValidator.validate_confirmation(password, confirmation)
        student = self.get_student(student_id)
        student.change_password(password, confirmation)
        self.database.update(student)
