from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from uniapp.storage.database import Database
from uniapp.services.student_service import StudentService
from uniapp.cli.app import CLIUniApp


class StudentWorkflowTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.path = Path(directory.name) / "students.data"
        self.db = Database(self.path)
        self.service = StudentService(self.db)

    def register(self):
        return self.service.register("Manish", "manish@university.com", "Example123")

    def test_register_restart_login(self):
        student = self.register()
        restarted = StudentService(Database(self.path))
        self.assertEqual(restarted.login(student.email, student.password).id, student.id)
        for email, password in ((student.email, "Wrong123"),
                                ("missing@university.com", student.password)):
            with self.assertRaisesRegex(ValueError, "Incorrect email or password"):
                restarted.login(email, password)

    def test_bad_registration_and_duplicate_leave_file_unchanged(self):
        self.register()
        before = self.path.read_bytes()
        for fields in (("Manish", "manish@university.com", "Example123"),
                       ("", "other@university.com", "Example123"),
                       ("Manish", "other@gmail.com", "Example123"),
                       ("Manish", "other@university.com", "weak")):
            with self.assertRaises(ValueError):
                self.service.register(*fields)
            self.assertEqual(before, self.path.read_bytes())

    def test_enrol_limit_remove_and_reenrol_persist(self):
        student = self.register()
        for _ in range(4):
            subject = self.service.enrol(student.id)
        before = self.path.read_bytes()
        with self.assertRaises(ValueError):
            self.service.enrol(student.id)
        with self.assertRaises(ValueError):
            self.service.remove_subject(student.id, "000")
        self.assertEqual(before, self.path.read_bytes())
        self.service.remove_subject(student.id, subject.id)
        self.assertEqual(len(Database(self.path).get_by_id(student.id).subjects), 3)
        self.service.enrol(student.id)
        self.assertEqual(len(Database(self.path).get_by_id(student.id).subjects), 4)

    def test_password_change_requires_confirmation_and_changes_login(self):
        student = self.register()
        for confirmation in (None, "Other123"):
            with self.assertRaises(ValueError):
                self.service.change_password(student.id, "Updated123", confirmation)
        self.service.login(student.email, student.password)
        self.service.change_password(student.id, "Updated123", "Updated123")
        restarted = StudentService(Database(self.path))
        restarted.login(student.email, "Updated123")
        with self.assertRaises(ValueError):
            restarted.login(student.email, "Example123")

    def test_write_failure_does_not_report_success_or_change_data(self):
        student = self.register()
        before = self.path.read_bytes()
        with patch("uniapp.storage.database.os.replace", side_effect=OSError("Disk error")):
            with self.assertRaises(OSError):
                self.service.enrol(student.id)
        self.assertEqual(before, self.path.read_bytes())

    def test_cli_register_login_enrol_change_password_and_exit(self):
        commands = iter(["S", "r", "Manish", "manish@university.com", "Example123",
                         "l", "manish@university.com", "Example123", "e", "s", "c",
                         "Updated123", "Updated123", "x", "x", "X"])
        output = []
        CLIUniApp(self.db, read=lambda prompt: next(commands), write=output.append).run()
        saved = self.service.login("manish@university.com", "Updated123")
        self.assertEqual(len(saved.subjects), 1)
        self.assertTrue(any("grade" in line for line in output))
        self.assertEqual(output[-1], "Goodbye.")

    def test_cli_failed_login_and_invalid_menu_recover(self):
        commands = iter(["?", "S", "l", "missing@university.com", "Wrong123", "x", "X"])
        output = []
        CLIUniApp(self.db, read=lambda prompt: next(commands), write=output.append).run()
        self.assertIn("Invalid option.", output)
        self.assertTrue(any("Incorrect email or password" in line for line in output))
        self.assertFalse(any("Welcome" in line for line in output))

    def test_cli_eof_exits_cleanly(self):
        def end_input(prompt):
            raise EOFError
        output = []
        CLIUniApp(self.db, read=end_input, write=output.append).run()
        self.assertIn("Goodbye.", output[-1])


if __name__ == "__main__":
    unittest.main()
