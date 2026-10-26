from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock

from uniapp.gui.app import GUIUniApp
from uniapp.services.student_service import StudentService
from uniapp.storage.database import Database


class GuiCallbackTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.path = Path(folder.name) / "students.data"
        self.service = StudentService(Database(self.path))
        self.student = self.service.register("Manish", "manish@university.com", "Example123")
        # Exercise real GUI callbacks without needing a desktop display.
        self.app = GUIUniApp.__new__(GUIUniApp)
        self.app.service = self.service
        self.app.student_id = None
        self.app.email = Mock()
        self.app.password = Mock()
        self.app.show_error = Mock()
        self.app.status = Mock()
        self.app.subject_window = None

    def test_blank_login_stays_logged_out(self):
        self.app.email.get.return_value = " "
        self.app.password.get.return_value = "Example123"
        self.app.login()
        self.assertIsNone(self.app.student_id)
        self.assertEqual(str(self.app.show_error.call_args.args[0]), "Email and password are required.")

    def test_invalid_format_and_wrong_password_stay_logged_out(self):
        for email, password in (("bad", "Example123"), (self.student.email, "Wrong123")):
            self.app.email.get.return_value = email
            self.app.password.get.return_value = password
            self.app.login()
            self.assertIsNone(self.app.student_id)
        self.assertEqual(self.app.show_error.call_count, 2)

    def test_gui_enrolments_are_saved_and_fifth_is_rejected(self):
        self.app.student_id = self.student.id
        for _ in range(4):
            self.app.enrol()
        before = self.path.read_bytes()
        self.app.enrol()
        self.app.show_error.assert_called_once()
        self.assertEqual(self.path.read_bytes(), before)
        saved = StudentService(Database(self.path)).login(self.student.email, self.student.password)
        self.assertEqual(len(saved.subjects), 4)

    def test_logged_out_enrol_does_nothing(self):
        before = self.path.read_bytes()
        self.app.enrol()
        self.assertEqual(self.path.read_bytes(), before)

    def test_removal_saves_and_refreshes_and_allows_reenrolment(self):
        self.app.student_id = self.student.id
        subjects = [self.service.enrol(self.student.id) for _ in range(4)]
        self.app.table = Mock()
        self.app.table.selection.return_value = ("selected",)
        self.app.table.item.return_value = (subjects[0].id, subjects[0].mark, subjects[0].grade)
        self.app.refresh_subjects = Mock()
        self.app.remove_subject()
        saved = Database(self.path).get_by_id(self.student.id)
        self.assertEqual([s.id for s in saved.subjects], [s.id for s in subjects[1:]])
        self.app.status.set.assert_called_with(f"Dropped {subjects[0].id}. Subjects enrolled: 3/4")
        self.assertEqual(len(self.app.refresh_subjects.call_args.args[0].subjects), 3)
        self.app.enrol()
        self.assertEqual(len(Database(self.path).get_by_id(self.student.id).subjects), 4)
        self.app.show_error.assert_not_called()

    def test_removal_without_selection_does_not_change_data(self):
        self.app.student_id = self.student.id
        self.app.table = Mock()
        self.app.table.selection.return_value = ()
        before = self.path.read_bytes()
        self.app.remove_subject()
        self.assertEqual(self.path.read_bytes(), before)
        self.app.show_error.assert_called_once_with("Select a subject to remove.")

    def test_removal_of_stale_selection_shows_existing_service_error(self):
        self.app.student_id = self.student.id
        subject = self.service.enrol(self.student.id)
        self.service.remove_subject(self.student.id, subject.id)
        self.app.table = Mock()
        self.app.table.selection.return_value = ("selected",)
        self.app.table.item.return_value = (subject.id, subject.mark, subject.grade)
        before = self.path.read_bytes()
        self.app.remove_subject()
        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual(str(self.app.show_error.call_args.args[0]), "Subject is not enrolled.")

    def test_logged_out_removal_does_nothing(self):
        before = self.path.read_bytes()
        self.app.remove_subject()
        self.assertEqual(self.path.read_bytes(), before)

    def test_subject_table_uses_saved_values(self):
        self.service.enrol(self.student.id)
        student = self.service.get_student(self.student.id)
        self.app.table = Mock()
        self.app.table.get_children.return_value = ["old-row"]
        self.app.average = Mock()
        self.app.refresh_subjects(student)
        subject = student.subjects[0]
        self.app.table.delete.assert_called_once_with("old-row")
        self.app.table.insert.assert_called_once_with("", "end", values=(subject.id, subject.mark, subject.grade))

    def test_logout_clears_session_and_child_windows(self):
        self.app.student_id = self.student.id
        window = Mock()
        self.app.enrolment_window = window
        self.app.root = Mock()
        self.app.logout()
        window.destroy.assert_called_once()
        self.assertIsNone(self.app.student_id)
        self.assertIsNone(self.app.subject_window)
        self.app.root.deiconify.assert_called_once()


if __name__ == "__main__":
    unittest.main()
