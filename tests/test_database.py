import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from uniapp.models.student import Student
from uniapp.storage.database import Database


class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "students.data"
        self.db = Database(self.path)

    def student(self, student_id=1, email="manish@university.com"):
        return Student(student_id, "Manish", email, "Example123")

    def test_missing_file_created(self):
        self.assertEqual(json.loads(self.path.read_text()), [])
        self.assertEqual(self.db.get_all(), [])

    def test_add_reload_and_lookup(self):
        student = self.student()
        student.enrol()
        self.db.add(student)
        restarted = Database(self.path)
        self.assertEqual(restarted.get_by_id(student.id).to_dict(), student.to_dict())
        self.assertEqual(restarted.find_by_email(student.email).id, student.id)
        self.assertIsNone(restarted.find_by_email("missing@university.com"))

    def test_enrol_remove_and_password_changes_survive_restart(self):
        student = self.student()
        self.db.add(student)
        student.enrol()
        subject = student.enrol()
        self.db.update(student)
        student = Database(self.path).get_by_id(student.id)
        student.remove_subject(subject.id)
        student.change_password("Updated123", "Updated123")
        self.db.update(student)
        restored = Database(self.path).get_by_id(student.id)
        self.assertEqual(restored.to_dict(), student.to_dict())
        self.assertEqual(len(restored.subjects), 1)

    def test_duplicate_id_or_email_does_not_change_file(self):
        self.db.add(self.student())
        before = self.path.read_bytes()
        for duplicate in (self.student(1, "other@university.com"), self.student(2)):
            with self.assertRaises(ValueError):
                self.db.add(duplicate)
            self.assertEqual(self.path.read_bytes(), before)

    def test_update_cannot_take_another_email(self):
        self.db.add(self.student())
        second = self.student(2, "other@university.com")
        self.db.add(second)
        before = self.path.read_bytes()
        second.email = "manish@university.com"
        with self.assertRaises(ValueError):
            self.db.update(second)
        self.assertEqual(self.path.read_bytes(), before)

    def test_remove_and_clear_persist(self):
        self.db.add(self.student())
        self.db.add(self.student(2, "other@university.com"))
        self.db.remove("000001")
        self.assertEqual([s.id for s in Database(self.path).get_all()], ["000002"])
        self.db.clear()
        self.assertEqual(Database(self.path).get_all(), [])

    def test_unknown_id_operations_leave_file_unchanged(self):
        before = self.path.read_bytes()
        for operation in (lambda: self.db.get_by_id("000001"),
                          lambda: self.db.remove("000001"),
                          lambda: self.db.update(self.student())):
            with self.assertRaises(ValueError):
                operation()
        self.assertEqual(self.path.read_bytes(), before)

    def test_corrupt_files_are_preserved(self):
        record = self.student().to_dict()
        invalid_subjects = dict(record, subjects={})
        for content in ("", "broken json", "{}", "[null]", "[{}]",
                        json.dumps([invalid_subjects]), json.dumps([record, record])):
            self.path.write_text(content)
            for operation in (lambda: Database(self.path), self.db.get_all,
                              self.db.clear, lambda: self.db.add(self.student())):
                with self.assertRaises(ValueError):
                    operation()
                self.assertEqual(self.path.read_text(), content)

    def test_invalid_utf8_is_preserved(self):
        self.path.write_bytes(b'\xff')
        with self.assertRaises(ValueError):
            self.db.get_all()
        self.assertEqual(self.path.read_bytes(), b'\xff')

    def test_failed_replace_preserves_file_and_cleans_temporary_file(self):
        self.db.add(self.student())
        before = self.path.read_bytes()
        with patch("uniapp.storage.database.os.replace", side_effect=OSError("Disk error")):
            with self.assertRaises(OSError):
                self.db.clear()
        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual(list(self.path.parent.iterdir()), [self.path])

    def test_separate_instances_read_latest_data(self):
        other = Database(self.path)
        self.db.add(self.student())
        other.add(self.student(2, "other@university.com"))
        self.assertEqual(len(self.db.get_all()), 2)
        detached = other.get_by_id("000001")
        detached.enrol()
        self.assertEqual(self.db.get_by_id("000001").subjects, [])

    def test_invalid_mutated_object_cannot_be_saved(self):
        student = self.student()
        self.db.add(student)
        before = self.path.read_bytes()
        student.password = "weak"
        with self.assertRaises(ValueError):
            self.db.update(student)
        self.assertEqual(self.path.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
