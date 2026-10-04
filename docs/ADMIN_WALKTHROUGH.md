# Admin walkthrough

Run `python -m uniapp` and choose A. Admin requires no login, as specified in the brief.

| Option | Action |
| --- | --- |
| s | List students with name, ID and email |
| g | Group students by overall average grade |
| p | Show PASS, FAIL and INCOMPLETE groups |
| r | Remove a student by their six-digit ID |
| c | Clear all students after typing y |
| x | Return to the university menu |

Reports never display passwords. Removal and clearing persist immediately. A missing student ID produces an error and returns to the menu. Any response other than y cancels clearing.

## Reporting rules

Grade grouping uses the current average without rounding before classification: below 50 Z, below 65 P, below 75 C, below 85 D, otherwise HD. A student with no subjects appears under NO RESULT. The displayed average is rounded to two decimal places only for readability.

For pass/fail, four subjects are required. An average of 50 or more passes; below 50 fails. Students with fewer than four subjects appear as INCOMPLETE. This is a working interpretation of the brief's four-subject wording and still needs tutor confirmation.

For example, marks 49, 50, 50, 50 average 49.75 and fail. Four marks of 50 average 50 and pass. Three marks of 100 are currently incomplete.

## Code

AdminService in `uniapp/services/admin_service.py` reads records through Database and builds groups. CLIUniApp displays those groups and collects menu choices. Every report reloads saved records, so it reflects subject changes.

The service itself has no confirmation prompt; CLIUniApp asks before calling clear. This keeps input/output separate from data operations.

## Verification and remaining work

59 tests pass across the project; one desktop GUI test is skipped without a display. Six new Admin tests cover boundary/fractional averages, incomplete enrolment, fresh reporting, persisted removal/clear, cancelled clearing, empty data and invalid IDs.

GUI is implemented and sample wording has been reviewed. See VERIFICATION.md for the remaining differences and desktop verification.
