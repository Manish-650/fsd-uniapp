# FSD UniApp

Group 03 university enrolment project using Python and a Tkinter desktop GUI.

## Status

The student CLI is runnable: register, login, enrol, remove subjects, show results and change passwords. All changes are saved to students.data. Admin now supports listing, grade grouping, pass/fail/incomplete reporting, removal and confirmed clearing. The student GUI provides login, enrolment, subject listing and error windows using the same data file. There are 59 passing tests and one desktop GUI test skipped in the headless development environment. CLI wording and interaction flow have been reviewed against the sample screenshots; remaining differences and desktop checks are recorded in [verification notes](docs/VERIFICATION.md).

Read [the Subject walkthrough](docs/SUBJECT_WALKTHROUGH.md) and [the Student walkthrough](docs/STUDENT_WALKTHROUGH.md) for explanations and examples. See [credential validation](docs/CREDENTIALS_WALKTHROUGH.md) for the current rules and assumptions. The [Database walkthrough](docs/DATABASE_WALKTHROUGH.md) explains saving, loading and a runnable example.

Run the student CLI from the repository root (Python 3):

```bash
python -m uniapp
```

On Windows, `py -m uniapp` also works when the Python launcher is installed. Choose S, then r to register or l to log in. Choose A for Admin; see [Admin instructions](docs/ADMIN_WALKTHROUGH.md). See [the CLI walkthrough](docs/CLI_WALKTHROUGH.md). Use fictional credentials: this local exercise stores passwords as plain text. Run only one instance at a time.

Run the GUI after registering through the CLI:

```bash
python -m uniapp.gui
```

A desktop display and Python with Tkinter are required. See [the GUI walkthrough](docs/GUI_WALKTHROUGH.md) for usage and manual checks.

Run checks from the repository root:

```bash
python -m unittest discover -s tests -v
```

## Structure

- `uniapp/models/`: Student and Subject domain classes.
- `uniapp/storage/`: Database class and students.data persistence.
- `uniapp/services/`: shared validation, enrolment and admin operations.
- `uniapp/cli/`: CLIUniApp menus and terminal output.
- `uniapp/gui/`: GUIUniApp login, enrolment, subject-list and exception windows.
- `tests/`: automated checks to add alongside implementation.
- `docs/`: decisions, development plan and contribution records.

Both interfaces must use the same business rules and students.data file. Runtime student records are excluded from Git.

## Development order

1. Resolve the outstanding rules in docs/PLAN.md.
2. Implement models and file persistence.
3. Verify register, save, restart, login, enrol and save.
4. Complete student and admin CLI functions.
5. Add the GUI and verify shared persisted data.
6. Verify sample I/O, package the project and rehearse the showcase.
