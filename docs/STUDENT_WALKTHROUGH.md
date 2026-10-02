# Student walkthrough

`uniapp/models/student.py` connects one student's details to their Subject objects.

## What the methods do

| Method/property | Purpose |
| --- | --- |
| `Student(...)` | Restore or construct a student with a known numeric ID. |
| `Student.create(...)` | Start at a random ID and skip IDs already used. Pass existing IDs as six-digit strings. |
| `subjects` | Return a copy of the enrolled-subject list. |
| `enrol(used_ids=())` | Generate and add a subject, stopping at four. Optional IDs exclude subjects used elsewhere. |
| `remove_subject(subject_id)` | Remove a subject using its three-digit string ID. |
| `average` | Calculate the mean of current subject marks; return None when empty. |
| `change_password(...)` | Validate and replace a password in memory; check confirmation when supplied. |
| `to_dict()` / `from_dict(...)` | Convert between objects and plain data without rerolling IDs or marks. |

The average is calculated when read, so it automatically reflects enrolment and removal. A failed fifth enrolment or unknown removal leaves the student's data unchanged. Returning a list copy prevents callers from adding a fifth subject by directly appending to the list.

## Try it

Run Python from the repository root:

```python
from uniapp.models.student import Student

student = Student.create("Manish", "manish@university.com", "Example123", set())
subject = student.enrol()
print(student.id)  # six digits, for example 000007
print(subject.id, subject.mark, subject.grade)
print(student.average)  # one subject: same as its mark
student.remove_subject(subject.id)
print(student.average)  # None
```

## Working assumptions and limits

- For now, average means the mean of currently enrolled subjects, without rounding. Empty enrolment has no average. Admin pass/fail and overall grading are still pending, including the brief's wording about four subjects.
- Subject IDs are unique within this student. Supplying all other used IDs to enrol supports global uniqueness if the tutor requires it.
- Student ID uniqueness depends on passing every existing student ID to create. Duplicate email checks will belong to registration/storage.
- Name, email and password cannot be blank. Email and password formats are now checked by the shared CredentialValidator during construction/restoration and password changes. Optional confirmation is checked before updating; future interfaces must request it. See CREDENTIALS_WALKTHROUGH.md for assumptions.
- Passwords are currently plain strings in the in-memory model and dictionary. Use fictional sample credentials only; file persistence is not implemented yet.
- Dictionary conversion does not save a file. Database is a later step.

## Tests

Run `python -m unittest discover -s tests -v` from the repository root. The ten Student tests cover ID collision/wraparound, empty enrolment, the four-subject limit, external ID exclusion, average updates, removal errors, list isolation, restoration, password changes and invalid data. The six existing Subject tests also pass.
