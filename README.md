# FSD UniApp

Group 03 university enrolment project using Python and a planned Tkinter desktop GUI.

## Status

Repository structure and planning notes only. The application is not implemented or runnable yet.

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


