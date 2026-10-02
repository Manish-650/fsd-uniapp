import unittest
from unittest.mock import patch

from uniapp.models.student import Student
from uniapp.models.subject import Subject


class StudentTests(unittest.TestCase):
    def make_student(self, subjects=None):
        return Student(7, "Manish", "manish@university.com", "Example123", subjects)

    def test_new_student(self):
        student = self.make_student()
        self.assertEqual(student.id, "000007")
        self.assertEqual(student.subjects, [])
        self.assertIsNone(student.average)

    def test_create_skips_collision_and_wraps(self):
        with patch("uniapp.models.student.random.randint", return_value=999999):
            student = Student.create("Manish", "manish@university.com", "Example123",
                                     {"999999", "000001"})
        self.assertEqual(student.id, "000002")

    def test_enrol_limit_and_reenrol_after_removal(self):
        student = self.make_student()
        for _ in range(4):
            student.enrol()
        before = student.to_dict()
        with self.assertRaises(ValueError):
            student.enrol()
        self.assertEqual(student.to_dict(), before)
        self.assertEqual(len({s.id for s in student.subjects}), 4)
        student.remove_subject(student.subjects[0].id)
        student.enrol()
        self.assertEqual(len(student.subjects), 4)

    def test_enrol_respects_external_ids(self):
        student = self.make_student()
        subject = student.enrol({f"{number:03d}" for number in range(1, 999)})
        self.assertEqual(subject.id, "999")

    def test_average_updates_on_enrol_and_remove(self):
        student = self.make_student([Subject(1, 50)])
        with patch("uniapp.models.subject.random.randint", return_value=81):
            added = student.enrol()
        self.assertEqual(student.average, 65.5)
        student.remove_subject(added.id)
        self.assertEqual(student.average, 50)
        student.remove_subject("001")
        self.assertIsNone(student.average)

    def test_unknown_removal_keeps_state(self):
        student = self.make_student([Subject(1, 50)])
        before = student.to_dict()
        with self.assertRaises(ValueError):
            student.remove_subject("999")
        self.assertEqual(student.to_dict(), before)

    def test_lists_are_not_shared(self):
        original = [Subject(1, 50)]
        student = self.make_student(original)
        original.clear()
        student.subjects.clear()
        self.assertEqual(len(student.subjects), 1)
        self.assertEqual(self.make_student().subjects, [])

    def test_round_trip_does_not_regenerate_values(self):
        student = self.make_student([Subject(1, 50), Subject(2, 81)])
        student.change_password("Updated123")
        with patch("random.randint") as randint, patch("random.choice") as choice:
            restored = Student.from_dict(student.to_dict())
        randint.assert_not_called()
        choice.assert_not_called()
        self.assertEqual(restored.to_dict(), student.to_dict())
        self.assertEqual(restored.average, 65.5)

    def test_blank_password_change_keeps_old_password(self):
        student = self.make_student()
        for value in ("", "  ", None):
            with self.assertRaises(ValueError):
                student.change_password(value)
        self.assertEqual(student.password, "Example123")

    def test_invalid_student_data(self):
        for student_id in (0, 1000000, True, "000007", 1.5):
            with self.subTest(student_id=student_id), self.assertRaises(ValueError):
                Student(student_id, "Manish", "manish@university.com", "Example123")
        for fields in (("", "a", "b"), ("a", " ", "b"), ("a", "b", None)):
            with self.assertRaises(ValueError):
                Student(1, *fields)
        for subjects in ([Subject(1, 50)] * 2, ["001"],
                         [Subject(i, 50) for i in range(1, 6)]):
            with self.assertRaises(ValueError):
                self.make_student(subjects)
        for student_id in ("7", "000000", "abcdef", "０００００７", 7):
            data = self.make_student().to_dict()
            data["id"] = student_id
            with self.assertRaises(ValueError):
                Student.from_dict(data)


if __name__ == "__main__":
    unittest.main()
