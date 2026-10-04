"""Terminal menus following the assignment's sample wording."""

from uniapp.services.student_service import StudentService
from uniapp.services.admin_service import AdminService
from uniapp.services.credential_validator import CredentialValidator


class CLIUniApp:
    INDENT = "        "

    def __init__(self, database, read=input, write=print):
        self.service = StudentService(database)
        self.admin = AdminService(database)
        self.read = read
        self.write = write

    def say(self, message, level=1):
        self.write(self.INDENT * level + message)

    def ask(self, message, level=1):
        return self.read(self.INDENT * level + message)

    def run(self):
        try:
            while True:
                choice = self.ask("University System: (A)dmin, (S)tudent, or X : ", 0).upper()
                if choice == "X":
                    self.say("Thank You", 0)
                    return
                if choice == "S":
                    self.student_menu()
                elif choice == "A":
                    self.admin_menu()
                else:
                    self.say("Invalid option.", 0)
        except (EOFError, KeyboardInterrupt):
            self.say("\nThank You", 0)

    def credentials(self):
        while True:
            email = self.ask("Email: ")
            password = self.ask("Password: ")
            try:
                CredentialValidator.validate_email(email)
                CredentialValidator.validate_password(password)
            except ValueError:
                self.say("Incorrect email or password format")
                continue
            self.say("email and password formats acceptable")
            return email, password

    def student_menu(self):
        while True:
            choice = self.ask("Student System (l/r/x): ").lower()
            if choice == "x":
                return
            try:
                if choice == "r":
                    self.say("Student Sign Up")
                    email, password = self.credentials()
                    existing = self.service.database.find_by_email(email)
                    if existing is not None:
                        self.say(f"Student {existing.name} already exists")
                        continue
                    name = self.ask("Name: ")
                    student = self.service.register(name, email, password)
                    self.say(f"Enrolling Student {student.name}")
                elif choice == "l":
                    self.say("Student Sign In")
                    email, password = self.credentials()
                    # Only a credential mismatch gets the sample's account error.
                    # File errors must remain visible instead of appearing as bad login.
                    student = self.service.database.find_by_email(email)
                    if student is None or student.password != password:
                        self.say("Student does not exist")
                        continue
                    student = self.service.login(email, password)
                    self.enrolment_menu(student.id)
                else:
                    self.say("Invalid option.")
            except (ValueError, OSError) as error:
                self.say(f"Error: {error}")

    def enrolment_count(self, student_id):
        count = len(self.service.get_student(student_id).subjects)
        self.say(f"You are now enrolled in {count} out of 4 subjects", 2)

    def change_password(self, student_id):
        self.say("Updating Password", 2)
        password = self.ask("New Password: ", 2)
        CredentialValidator.validate_password(password)
        while True:
            confirmation = self.ask("Confirm Password: ", 2)
            if password == confirmation:
                self.service.change_password(student_id, password, confirmation)
                return
            self.say("Password does not match - try again", 2)

    def enrolment_menu(self, student_id):
        while True:
            choice = self.ask("Student Course Menu (c/e/r/s/x): ", 2).lower()
            if choice == "x":
                return
            try:
                if choice == "e":
                    if len(self.service.get_student(student_id).subjects) >= 4:
                        self.say("Students are allowed to enrol in 4 subjects only", 2)
                        continue
                    subject = self.service.enrol(student_id)
                    self.say(f"Enrolling in Subject-{subject.id}", 2)
                    self.enrolment_count(student_id)
                elif choice == "r":
                    subject_id = self.ask("Remove Subject by ID: ", 2)
                    self.service.remove_subject(student_id, subject_id)
                    self.say(f"Dropping Subject-{subject_id}", 2)
                    self.enrolment_count(student_id)
                elif choice == "c":
                    self.change_password(student_id)
                elif choice == "s":
                    student = self.service.get_student(student_id)
                    self.say(f"Showing {len(student.subjects)} subjects", 2)
                    for subject in student.subjects:
                        self.say(f"[ Subject::{subject.id} -- mark = {subject.mark} "
                                 f"-- grade = {subject.grade:>2} ]", 2)
                else:
                    self.say("Invalid option.", 2)
            except (ValueError, OSError) as error:
                self.say(f"Error: {error}", 2)

    def show_students(self, students):
        self.say("Student List")
        if not students:
            self.say("< Nothing to Display >", 2)
        for student in students:
            self.say(f"{student.name} :: {student.id} --> Email: {student.email}")

    def result_text(self, student):
        average = "N/A" if student.average is None else f"{student.average:.2f}"
        return (f"{student.name} :: {student.id} --> GRADE: "
                f"{self.admin.grade(student)} - MARK: {average}")

    def show_groups(self, groups, include_empty=False):
        for label, students in groups.items():
            if students or include_empty:
                values = ", ".join(self.result_text(student) for student in students)
                self.say(f"{label} --> [{values}]")

    def admin_menu(self):
        while True:
            choice = self.ask("Admin System (c/g/p/r/s/x): ").lower()
            if choice == "x":
                return
            try:
                if choice == "s":
                    self.show_students(self.admin.list_students())
                elif choice == "g":
                    self.say("Grade Grouping")
                    groups = self.admin.group_by_grade()
                    if not any(groups.values()):
                        self.say("< Nothing to Display >", 2)
                    self.show_groups(groups)
                elif choice == "p":
                    self.say("PASS/FAIL Partition")
                    groups = self.admin.partition()
                    self.show_groups({label: groups[label] for label in ("FAIL", "PASS")}, True)
                    if groups["INCOMPLETE"]:
                        self.show_groups({"INCOMPLETE": groups["INCOMPLETE"]})
                elif choice == "r":
                    student_id = self.ask("Remove by ID: ")
                    if not any(s.id == student_id for s in self.admin.list_students()):
                        self.say(f"Student {student_id} does not exist")
                        continue
                    self.admin.remove(student_id)
                    self.say(f"Removing Student {student_id} Account")
                elif choice == "c":
                    self.say("Clearing students database")
                    confirmation = self.ask("Are you sure you want to clear the database (Y)ES/(N)O: ").upper()
                    if confirmation == "Y":
                        self.admin.clear()
                        self.say("Students data cleared")
                else:
                    self.say("Invalid option.")
            except (ValueError, OSError) as error:
                self.say(f"Error: {error}")
