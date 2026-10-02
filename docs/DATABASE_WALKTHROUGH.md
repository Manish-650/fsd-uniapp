# Database walkthrough

Database connects Student objects to the file students.data. The file contains JSON, a readable representation of lists and dictionaries. No extra Python packages are needed.

## Main methods

| Method | Purpose |
| --- | --- |
| Database() | Open students.data at the repository root; create it if missing |
| get_all() | Read all students as fresh objects |
| get_by_id(id) | Find a student or raise an error |
| find_by_email(email) | Find a student or return None |
| add(student) | Save a new student, rejecting duplicate IDs/emails |
| update(student) | Replace the record with that student's ID |
| remove(id) | Delete one student |
| clear() | Save an empty list |

Emails are compared exactly, including letter case. This is a working identity rule to keep consistent with future registration/login.

## Saving a change

Read the student, call a Student method, then call Database.update. Changing an object alone does not change the file.

The database validates every record before saving. It writes the new data to a temporary file, then replaces students.data. If replacement fails, the old file stays intact and the temporary file is removed.

A missing file is created as an empty list. An existing blank or damaged file raises an error and is preserved for repair. Even clear refuses to silently erase unreadable data.

## Try this from the repository root

This example uses a temporary folder and removes its sample file automatically when finished.

```python
from pathlib import Path
from tempfile import TemporaryDirectory

from uniapp.models.student import Student
from uniapp.storage.database import Database

with TemporaryDirectory() as folder:
    filename = Path(folder) / "students.data"
    db = Database(filename)
    used_ids = {student.id for student in db.get_all()}
    student = Student.create("Manish", "manish@university.com", "Example123", used_ids)
    db.add(student)

    student = db.get_by_id(student.id)
    subject = student.enrol()
    db.update(student)

    reopened = Database(filename)
    saved = reopened.get_by_id(student.id)
    print(saved.name, len(saved.subjects))  # Manish 1
    print(saved.subjects[0].mark == subject.mark)  # True
```

Calling Database() without a filename uses the shared project-root file, regardless of the terminal's working folder. For a custom filename, its parent folder must already exist.

## Current limits

- Login and registration workflows still need to connect validation, ID generation and these database methods.
- The future CLI and GUI must save after every successful mutation.
- Use one running application at a time. This simple file store does not lock against simultaneous writers.
- Reload a student before editing: updating an old object replaces that student's entire record.
- Passwords remain plain text in this exercise's file. Use fictional credentials; this is not a production account store.
- The JSON format is a working choice pending any tutor-specific file-format requirement.

## Verification

Run `python -m unittest discover -s tests -v`. All 35 tests pass, including 12 database tests for creation, reloading, enrolment/password persistence, deletion, duplicate rejection, corrupt files, detached objects and a simulated failed replacement.
