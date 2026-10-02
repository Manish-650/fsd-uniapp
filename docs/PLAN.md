# Implementation plan

## Confirmed requirements

Python is the chosen language. Use Student, Subject and Database classes. CLIUniApp includes university, student, enrolment and admin menus. GUIUniApp is a separate student-only application for existing registered students.

Student IDs must be unique and formatted 000001-999999. Subject IDs use 001-999. Subject marks are generated once at enrolment, between 25 and 100 inclusive. Enrolment is limited to four subjects. Persist all mutations to students.data, create it when absent, and reload saved records for login and admin reporting.

The GUI requires login, enrolment, subject-list and exception windows. The CLI output must match the sample wording and indentation. Admin access does not require login.

## Changes from Part 1

- Use Database for the persistence responsibilities previously assigned to StudentDataStore.
- Admin grouping uses an overall student average and grade rather than individual subject results.
- Add the explicit subject-list and exception GUI windows.
- Standardise the filename as students.data throughout.

## Clarifications before implementation

- Password rule: the text says at least five letters followed by at least three digits, starting uppercase, but the sample rejects Hello123. Ask the tutor which interpretation to use.
- Define overall result behaviour for zero, one, two or three enrolled subjects; the pass rule mentions all four subjects.
- Confirm whether subject-ID uniqueness is global or per student and how exhausted IDs are handled.
- Confirm the precise email pattern beyond the university.com domain.
- Confirm acceptable serialisation format. No database or file format has been selected yet.

## Verification checklist

- Registration rejects duplicates and invalid credentials.
- Login reads persisted data; wrong credentials fail clearly.
- Changes survive application restart.
- Fifth-subject attempts fail without changing saved records.
- Removing an unknown subject/student is handled.
- Password confirmation and validation work; updated credentials survive restart.
- Grade boundaries and average recalculation are correct.
- Admin grouping, partitioning, removal and clear operate on file data.
- Empty data, missing file and malformed file are handled without silent data loss.
- GUI handles blank fields, invalid email, incorrect credentials and enrolment limits.
- CLI-created accounts work in the GUI, and GUI changes appear in the CLI after reload.

## Delivery

One integrated group ZIP, with accurate contributions and run instructions. Confirm the exact Canvas deadline (brief: Sunday Week 13) and lab number before naming group<group-number>-Cmp1<lab-number>.zip. All members must attend the Week 13 in-person showcase and explain their own work.

## Credential implementation decision

The shared CredentialValidator currently follows the written password rule: `[A-Z][A-Za-z]{4,}[0-9]{3,}`. It accepts Hello123 despite the conflicting example; tutor confirmation remains outstanding. Email uses common ASCII local-part characters (letters, digits, underscore, plus, percent, hyphen and separated dots) with the exact lowercase @university.com domain. Leading, trailing and consecutive dots, spaces and surrounding whitespace are rejected. This email pattern is a working assumption, not a confirmed additional requirement. Student construction/restoration and password changes use the validator. Password confirmation is supported when supplied; both future interfaces must request it. Authentication, duplicate-email checks and persistence remain pending.
