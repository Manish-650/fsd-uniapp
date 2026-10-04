from pathlib import Path
import tempfile
import unittest

from uniapp.models.student import Student
from uniapp.models.subject import Subject
from uniapp.storage.database import Database
from uniapp.services.admin_service import AdminService
from uniapp.cli.app import CLIUniApp


class AdminTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.path = Path(directory.name) / "students.data"
        self.db = Database(self.path)
        self.admin = AdminService(self.db)

    def add(self, student_id, marks):
        student = Student(student_id, "Student", f"student{student_id}@university.com",
                          "Example123", [Subject(i + 1, mark) for i, mark in enumerate(marks)])
        self.db.add(student)
        return student

    def test_grade_boundaries_and_fractional_average(self):
        for i, (marks, grade) in enumerate((([49], "Z"), ([50], "P"), ([64, 65], "P"),
                                           ([65], "C"), ([74, 75], "C"), ([75], "D"),
                                           ([84, 85], "D"), ([85], "HD"), ([], "NO RESULT")), 1):
            student = self.add(i, marks)
            self.assertEqual(self.admin.grade(student), grade)
            self.assertIn(student.id, [s.id for s in self.admin.group_by_grade()[grade]])

    def test_partition_four_subject_boundary_and_incomplete(self):
        self.add(1, [49, 50, 50, 50])
        self.add(2, [50, 50, 50, 50])
        self.add(3, [100, 100, 100])
        self.add(4, [])
        groups = self.admin.partition()
        self.assertEqual([s.id for s in groups["FAIL"]], ["000001"])
        self.assertEqual([s.id for s in groups["PASS"]], ["000002"])
        self.assertEqual([s.id for s in groups["INCOMPLETE"]], ["000003", "000004"])

    def test_reports_reload_and_do_not_modify_file(self):
        self.add(1, [50] * 4)
        student = self.db.get_by_id("000001")
        student.remove_subject("001")
        self.db.update(student)
        before = self.path.read_bytes()
        self.assertEqual(len(self.admin.partition()["INCOMPLETE"]), 1)
        self.admin.group_by_grade()
        self.admin.list_students()
        self.assertEqual(before, self.path.read_bytes())

    def test_remove_and_clear_survive_reopen(self):
        self.add(1, [])
        self.add(2, [85])
        self.admin.remove("000001")
        self.assertEqual(len(Database(self.path).get_all()), 1)
        with self.assertRaises(ValueError):
            self.admin.remove("000001")
        self.admin.clear()
        self.assertEqual(Database(self.path).get_all(), [])

    def test_cli_reports_remove_cancel_clear_and_confirm_clear(self):
        self.add(1, [50] * 4)
        self.add(2, [])
        commands = iter(["A", "s", "g", "p", "r", "000001", "c", "n", "x", "X"])
        output = []
        CLIUniApp(self.db, lambda prompt: next(commands), output.append).run()
        self.assertEqual([s.id for s in self.db.get_all()], ["000002"])
        self.assertNotIn("        Students data cleared", output)
        self.assertFalse(any("Example123" in line for line in output))
        commands = iter(["A", "c", "y", "x", "X"])
        CLIUniApp(self.db, lambda prompt: next(commands), output.append).run()
        self.assertEqual(Database(self.path).get_all(), [])

    def test_empty_reports_and_bad_id_recover(self):
        self.assertTrue(all(not group for group in self.admin.group_by_grade().values()))
        commands = iter(["A", "s", "r", "bad", "?", "x", "X"])
        output = []
        CLIUniApp(self.db, lambda prompt: next(commands), output.append).run()
        self.assertIn("                < Nothing to Display >", output)
        self.assertIn("        Student bad does not exist", output)
        self.assertEqual(output[-1], "Thank You")


if __name__ == "__main__":
    unittest.main()
