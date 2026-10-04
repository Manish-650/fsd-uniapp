# Verification notes

## Automated result

60 tests discovered: 59 passed and one skipped. The skipped test opens real Tkinter windows and cannot run in the current environment, which has Tkinter but no graphical display or Xvfb.

Run all tests from the repository root:

```bash
python -m unittest discover -s tests -v
```

Run the desktop test alone on a laptop with Tkinter:

```bash
python -m unittest discover -s tests -p test_gui_desktop.py -v
```

The desktop test uses temporary fictional records. It does not clear your normal students.data.

## Sample comparison

The assignment's screenshots on pages 3-7 were visually reviewed.

Updated: university/student/course/admin prompts, Thank You on exit, email/password before name at registration, repeated credential-format prompts, duplicate-student and login messages, enrolment counts, subject rows, confirmation retries, student list, grade groups, pass/fail lists, missing IDs, and clear confirmation.

Four transcript tests now check menu navigation exactly, registration retry/order, subject formatting/password confirmation and empty Admin reports.

## Explicit remaining differences

- Eight spaces are used per menu level. Screenshot scaling/cropping prevents a reliable claim about exact whitespace width.
- Output is plain text; the example's cyan/yellow/red terminal colours are not reproduced.
- All subject IDs remain three digits, including enrolment messages; one example message displays 97 while its subject row shows 097.
- Hello123 is accepted under the written password rule despite the contradictory sample.
- Students with fewer than four subjects appear in INCOMPLETE; empty enrolment has NO RESULT. Tutor clarification remains needed.
- Invalid choices, invalid new-password formats, missing subjects and file errors use readable fallback errors where no complete sample behaviour was supplied.
- Random IDs and marks will differ from the examples by design.

## Desktop verification still open

The real-widget test is ready but was not run successfully here. Use the GUI walkthrough's manual checklist to verify appearance, keyboard/mouse input, error dialogs and closing windows. Confirm no controls are clipped on your screen.

No final submission-ready or exact-output-equivalence claim is made. Resolve the documented rule ambiguities, complete desktop verification and enter accurate member contributions before packaging.
