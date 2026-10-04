# Student CLI walkthrough

Run from the downloaded repository folder:

```bash
python -m uniapp
```

On Windows you can also use `py -m uniapp`. No extra packages are required.

## Try the student flow

1. Choose S at the university menu.
2. Choose r and enter a name, fictional university email such as manish@university.com, and a sample password such as Example123.
3. Choose l and enter the same email and password.
4. Choose e to enrol; choose s to see subject IDs, marks, grades and average.
5. Choose r and enter a displayed three-digit subject ID to remove it.
6. Choose c to change the password, then enter it again to confirm.
7. Choose x to leave each submenu; choose X at the university menu to quit.
8. Restart and log in with the latest password. The saved subjects keep their IDs and marks.

A fifth enrolment is rejected. Invalid credentials, unknown subject IDs and mismatched confirmation show errors and allow another attempt.

## How the code connects

- `uniapp/__main__.py` opens the data file and starts CLIUniApp.
- `uniapp/cli/app.py` collects input and prints results.
- `uniapp/services/student_service.py` coordinates validation, Student operations and Database calls.
- Database writes every successful change before the service returns.
- The logged-in menu keeps the student ID and reloads the current record for each operation, avoiding an old in-memory copy.

Registration validates credentials, rejects an existing email, generates an unused student ID and saves. Login validates the input format and compares credentials against the saved account. Unknown accounts and incorrect passwords both raise the same error.

The service is reusable by the future GUI. It is an internal application layer, not a network API or an independent authorization boundary; the interface must only pass the logged-in student's ID for student actions.

## Files and limits

The default students.data is at the repository root. Use `python -m uniapp --data /path/to/students.data` for a separate demonstration file; its parent folder must exist. Do not put real passwords in this teaching app. Terminal passwords are currently visible while entered, and saved passwords are plain text.

Use one application instance at a time. Subject IDs are currently unique within each student's enrolments. Existing documented password, email and average assumptions still apply.

Admin is not implemented yet; selecting A reports that status. GUI and exact wording/indentation matching against the sample screenshots remain pending. This milestone is a runnable student workflow, not the finished assessment.

## Verification

43 tests pass with `python -m unittest discover -s tests -v`. New tests cover registration/restart/login, duplicates, invalid input, persisted subject changes, password confirmation, failed saves, CLI recovery and end-of-input. A separate-process smoke check also verified registration followed by restart, login, enrolment and display.
