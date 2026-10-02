"""Student details and subject enrolments."""

import random

from uniapp.models.subject import Subject


class Student:
    MAX_SUBJECTS = 4

    def __init__(self, student_id, name, email, password, subjects=None):
        if type(student_id) is not int or not 1 <= student_id <= 999999:
            raise ValueError("Student ID must be an integer from 1 to 999999.")
        for label, value in (("Name", name), ("Email", email), ("Password", password)):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{label} cannot be blank.")
        subjects = list(subjects) if subjects is not None else []
        if len(subjects) > self.MAX_SUBJECTS:
            raise ValueError("A student can enrol in at most four subjects.")
        if any(not isinstance(subject, Subject) for subject in subjects):
            raise ValueError("Enrolments must be Subject objects.")
        if len({subject.id for subject in subjects}) != len(subjects):
            raise ValueError("A student cannot have duplicate subject IDs.")
        self.id = f"{student_id:06d}"
        self.name = name.strip()
        self.email = email.strip()
        self.password = password
        self._subjects = subjects

    @property
    def subjects(self):
        # A copy prevents callers from bypassing the four-subject limit.
        return list(self._subjects)

    @property
    def average(self):
        if not self._subjects:
            return None
        return sum(subject.mark for subject in self._subjects) / len(self._subjects)

    @classmethod
    def create(cls, name, email, password, used_ids):
        """Exclude existing six-digit ID strings supplied by the caller."""
        used_ids = set(used_ids)
        student_id = random.randint(1, 999999)
        # Scan from a random starting point; even a nearly full range terminates.
        for _ in range(999999):
            if f"{student_id:06d}" not in used_ids:
                return cls(student_id, name, email, password)
            student_id = student_id % 999999 + 1
        raise ValueError("No student IDs are available.")

    def enrol(self, used_ids=()):
        if len(self._subjects) >= self.MAX_SUBJECTS:
            raise ValueError("A student can enrol in at most four subjects.")
        excluded_ids = set(used_ids) | {subject.id for subject in self._subjects}
        subject = Subject.create(excluded_ids)
        self._subjects.append(subject)
        return subject

    def remove_subject(self, subject_id):
        for subject in self._subjects:
            if subject.id == subject_id:
                self._subjects.remove(subject)
                return subject
        raise ValueError("Subject is not enrolled.")

    def change_password(self, new_password):
        # Credential format validation belongs to the shared validator (next step).
        if not isinstance(new_password, str) or not new_password.strip():
            raise ValueError("Password cannot be blank.")
        self.password = new_password

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "subjects": [subject.to_dict() for subject in self._subjects],
        }

    @classmethod
    def from_dict(cls, data):
        student_id = data["id"]
        if (not isinstance(student_id, str) or len(student_id) != 6
                or not student_id.isascii() or not student_id.isdigit()):
            raise ValueError("Saved student ID must contain six digits.")
        return cls(int(student_id), data["name"], data["email"], data["password"],
                   [Subject.from_dict(subject) for subject in data["subjects"]])
