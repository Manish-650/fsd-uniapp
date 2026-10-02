"""Read and write student records in students.data."""

import json
import os
from pathlib import Path
import tempfile

from uniapp.models.student import Student


class Database:
    def __init__(self, filename=None):
        # Both interfaces use the same file even from different working folders.
        self.path = (Path(filename) if filename is not None else
                     Path(__file__).resolve().parents[2] / "students.data")
        if not self.path.exists():
            with self.path.open("x", encoding="utf-8") as file:
                file.write("[]\n")
        self.get_all()  # Reject damaged files immediately; never reset them.

    @staticmethod
    def _decode_records(records):
        if not isinstance(records, list):
            raise ValueError("Student records must be a list.")
        students = []
        ids = set()
        emails = set()
        for record in records:
            if not isinstance(record, dict) or set(record) != {
                    "id", "name", "email", "password", "subjects"}:
                raise ValueError("Invalid student record fields.")
            if not isinstance(record["subjects"], list):
                raise ValueError("Subjects must be a list.")
            for subject in record["subjects"]:
                if not isinstance(subject, dict) or set(subject) != {"id", "mark"}:
                    raise ValueError("Invalid subject record fields.")
            student = Student.from_dict(record)
            if student.id in ids:
                raise ValueError("Duplicate student ID.")
            if student.email in emails:
                raise ValueError("Email is already registered.")
            ids.add(student.id)
            emails.add(student.email)
            students.append(student)
        return students

    def get_all(self):
        """Return fresh objects; changing them requires an explicit update."""
        try:
            records = json.loads(self.path.read_text(encoding="utf-8"))
            return self._decode_records(records)
        except (ValueError, TypeError, KeyError) as error:
            raise ValueError(f"Invalid student data in {self.path.name}: {error}") from error

    def get_by_id(self, student_id):
        for student in self.get_all():
            if student.id == student_id:
                return student
        raise ValueError("Student not found.")

    def find_by_email(self, email):
        for student in self.get_all():
            if student.email == email:
                return student
        return None

    def _write(self, students):
        records = [student.to_dict() for student in students]
        self._decode_records(records)  # Validate before touching the saved file.
        temporary_path = None
        try:
            with tempfile.NamedTemporaryFile(
                    mode="w", encoding="utf-8", dir=self.path.parent,
                    prefix=self.path.name + ".", suffix=".tmp", delete=False) as file:
                temporary_path = Path(file.name)
                json.dump(records, file, indent=2, ensure_ascii=False)
                file.write("\n")
                file.flush()
                os.fsync(file.fileno())
            os.replace(temporary_path, self.path)
        finally:
            if temporary_path is not None and temporary_path.exists():
                temporary_path.unlink()

    def add(self, student):
        students = self.get_all()
        students.append(student)
        self._write(students)

    def update(self, student):
        students = self.get_all()
        for index, saved in enumerate(students):
            if saved.id == student.id:
                students[index] = student
                self._write(students)
                return
        raise ValueError("Student not found.")

    def remove(self, student_id):
        students = self.get_all()
        for student in students:
            if student.id == student_id:
                students.remove(student)
                self._write(students)
                return
        raise ValueError("Student not found.")

    def clear(self):
        self.get_all()  # Do not silently erase a file that cannot be read.
        self._write([])
