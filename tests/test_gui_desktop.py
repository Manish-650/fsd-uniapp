"""Real widget integration test: automatically skipped without a display."""
from pathlib import Path
import tempfile
import unittest
import tkinter as tk

from uniapp.cli.app import CLIUniApp
from uniapp.gui.app import GUIUniApp
from uniapp.storage.database import Database


class GuiDesktopTests(unittest.TestCase):
    def test_cli_account_gui_enrolment_and_logout(self):
        try:
            root = tk.Tk()
        except tk.TclError as error:
            self.skipTest(f'Desktop display unavailable: {error}')
        self.addCleanup(root.destroy)
        with tempfile.TemporaryDirectory() as folder:
            db = Database(Path(folder) / 'students.data')
            commands = iter(['S', 'r', 'manish@university.com', 'Example123', 'Manish', 'x', 'X'])
            CLIUniApp(db, lambda prompt: next(commands), lambda text: None).run()
            app = GUIUniApp(root, db)
            root.update()
            app.email.insert(0, 'manish@university.com')
            app.password.insert(0, 'Example123')
            app.login()
            root.update()
            self.assertIsNotNone(app.student_id)
            self.assertEqual(root.state(), 'withdrawn')
            app.show_subjects()
            root.update()
            for _ in range(4):
                app.enrol()
                root.update()
            self.assertEqual(len(app.table.get_children()), 4)
            before = db.path.read_bytes()
            app.enrol()
            root.update()
            self.assertTrue(app.error_window.winfo_exists())
            self.assertEqual(db.path.read_bytes(), before)
            app.error_window.destroy()
            student_id = app.student_id
            app.logout()
            root.update()
            self.assertIsNone(app.student_id)
            self.assertEqual(root.state(), 'normal')
            self.assertEqual(len(Database(db.path).get_by_id(student_id).subjects), 4)
