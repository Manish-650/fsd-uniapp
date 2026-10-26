# GUI walkthrough

## Run

From the repository folder, first run `python -m uniapp`, choose S then r and register a fictional student account. Exit the CLI, then run:

```bash
python -m uniapp.gui
```

On Windows, `py -m uniapp.gui` can be used with the Python launcher. Python must include Tkinter and a desktop display must be available. Both applications default to the same project-root students.data file. Both support --data for a custom path; use the same path in each app.

## Four windows

1. Login: enter an existing student's email/password. Password input is masked.
2. Enrolment: enrol in a subject, view subjects or log out.
3. Subjects: shows IDs, marks and grades from saved records, plus the current average. Select a row and click **Remove selected subject** to drop it. The removal saves immediately and updates the table, average and enrolment count. Removing without selecting a row displays an error.
4. Error: displays blank-input, invalid-credential, enrolment-limit and file errors.

Registration is only in the CLI, as required. The GUI is student-only. Each enrolment saves immediately through StudentService. If the subject window is open, it refreshes after enrolment. Closing the enrolment window logs out and closes its child windows.

## How the code works

uniapp/gui/app.py contains GUIUniApp. Buttons call login, enrol, show_subjects, remove_subject and logout. The existing StudentService performs validation and saved-data operations. No second copy of the enrolment rules or separate GUI database is introduced.

uniapp/gui/__main__.py opens the database, creates the root Tk window and starts its event loop.

## Desktop check still required

All 64 automated tests pass, including ten GUI callback tests and a real Tkinter widget integration test. Manual appearance and mouse/keyboard checks remain useful.

On your desktop:

- Try blank fields, a malformed email and a wrong password; each should open an error window and keep you logged out.
- Log in with a CLI-created account.
- Open the subject list, then enrol up to four times. The list and count should refresh.
- Attempt a fifth enrolment; an error should appear and no extra subject should be saved.
- Select a subject and remove it; confirm the list, average and count update, and that you can enrol again.
- Log out with the subject window open; both account windows should close.
- Log in again and confirm the same IDs and marks appear.
- Exit the GUI, run the CLI and confirm the same subjects appear there.
- Check the windows fit your screen, all buttons are visible, and closing windows works as described.

64 automated tests pass, including ten display-free GUI callback tests and one real-widget integration test. Run `python -m unittest discover -s tests -p test_gui_desktop.py -v` on your laptop to exercise CLI registration, GUI login, real subject widgets, four enrolments, fifth-subject error, removal, re-enrolment and logout. Actual appearance still needs the checklist above. CLI sample wording has been reviewed; documented differences and tutor clarifications remain in VERIFICATION.md.
