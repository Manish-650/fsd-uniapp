from pathlib import Path
import tempfile
import unittest

from uniapp.cli.app import CLIUniApp
from uniapp.models.student import Student
from uniapp.models.subject import Subject
from uniapp.storage.database import Database


class CliSampleTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.db = Database(Path(folder.name) / 'students.data')

    def run_commands(self, commands):
        commands = iter(commands)
        transcript = []
        def read(prompt):
            answer = next(commands)
            transcript.append(prompt + answer)
            return answer
        CLIUniApp(self.db, read, transcript.append).run()
        return transcript

    def test_menu_navigation_exact_transcript(self):
        self.assertEqual(self.run_commands(['A', 'x', 'S', 'x', 'X']), [
            'University System: (A)dmin, (S)tudent, or X : A',
            '        Admin System (c/g/p/r/s/x): x',
            'University System: (A)dmin, (S)tudent, or X : S',
            '        Student System (l/r/x): x',
            'University System: (A)dmin, (S)tudent, or X : X',
            'Thank You'])

    def test_registration_retries_format_before_name(self):
        output = self.run_commands(['S', 'r', 'bad', 'weak',
                                    'manish@university.com', 'Example123', 'Manish', 'x', 'X'])
        self.assertEqual(output[2:10], [
            '        Student Sign Up', '        Email: bad', '        Password: weak',
            '        Incorrect email or password format',
            '        Email: manish@university.com', '        Password: Example123',
            '        email and password formats acceptable', '        Name: Manish'])
        self.assertEqual(len(self.db.get_all()), 1)

    def test_password_confirmation_retries_and_subject_output(self):
        self.db.add(Student(1, 'Manish', 'manish@university.com', 'Example123', [Subject(97, 85)]))
        output = self.run_commands(['S', 'l', 'manish@university.com', 'Example123',
                                    's', 'c', 'Updated123', 'wrong', 'Updated123', 'x', 'x', 'X'])
        self.assertIn('                [ Subject::097 -- mark = 85 -- grade = HD ]', output)
        self.assertIn('                Password does not match - try again', output)
        self.assertEqual(self.db.get_by_id('000001').password, 'Updated123')

    def test_empty_admin_sample_output(self):
        output = self.run_commands(['A', 's', 'g', 'p', 'x', 'X'])
        self.assertIn('        Student List', output)
        self.assertIn('        Grade Grouping', output)
        self.assertIn('        PASS/FAIL Partition', output)
        self.assertIn('        FAIL --> []', output)
        self.assertIn('        PASS --> []', output)
        self.assertEqual(output.count('                < Nothing to Display >'), 2)


if __name__ == '__main__':
    unittest.main()
