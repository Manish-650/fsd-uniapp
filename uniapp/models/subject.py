"""A subject enrolment and its result."""

import random


class Subject:
    def __init__(self, subject_id, mark):
        if type(subject_id) is not int or not 1 <= subject_id <= 999:
            raise ValueError("Subject ID must be an integer from 1 to 999.")
        if type(mark) is not int or not 25 <= mark <= 100:
            raise ValueError("Mark must be an integer from 25 to 100.")
        self.id = f"{subject_id:03d}"
        self.mark = mark

    @property
    def grade(self):
        # Derive the grade so it always agrees with the mark.
        if self.mark < 50:
            return "Z"
        elif self.mark < 65:
            return "P"
        elif self.mark < 75:
            return "C"
        elif self.mark < 85:
            return "D"
        return "HD"

    @classmethod
    def create(cls, used_ids):
        """Create an enrolment, excluding IDs supplied by the caller."""
        available_ids = [
            number for number in range(1, 1000)
            if f"{number:03d}" not in used_ids
        ]
        if not available_ids:
            raise ValueError("No subject IDs are available.")
        return cls(random.choice(available_ids), random.randint(25, 100))

    def to_dict(self):
        return {"id": self.id, "mark": self.mark}

    @classmethod
    def from_dict(cls, data):
        """Restore saved values without generating a new ID or mark."""
        subject_id = data["id"]
        if (not isinstance(subject_id, str) or len(subject_id) != 3
                or not subject_id.isascii() or not subject_id.isdigit()):
            raise ValueError("Saved subject ID must contain three digits.")
        return cls(int(subject_id), data["mark"])
