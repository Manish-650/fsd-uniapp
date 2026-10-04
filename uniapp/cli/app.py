"""Student and admin terminal interface."""

from uniapp.services.student_service import StudentService
from uniapp.services.admin_service import AdminService


class CLIUniApp:
    def __init__(self, database, read=input, write=print):
        self.service = StudentService(database)
        self.admin = AdminService(database)
        self.read = read
        self.write = write

    def run(self):
        try:
            while True:
                choice = self.read("University System: (A) Admin, (S) Student, (X) Exit: ").upper()
                if choice == "X":
                    self.write("Goodbye.")
                    return
                if choice == "S":
                    self.student_menu()
                elif choice == "A":
                    self.admin_menu()
                else:
                    self.write("Invalid option.")
        except (EOFError, KeyboardInterrupt):
            self.write("\nGoodbye.")

    def student_menu(self):
        while True:
            choice = self.read("    Student System: (l) login, (r) register, (x) exit: ").lower()
            if choice == "x":
                return
            try:
                if choice == "r":
                    name = self.read("    Name: ")
                    email = self.read("    Email: ")
                    password = self.read("    Password: ")
                    student = self.service.register(name, email, password)
                    self.write(f"    Registered {student.name} with ID {student.id}.")
                elif choice == "l":
                    email = self.read("    Email: ")
                    password = self.read("    Password: ")
                    student = self.service.login(email, password)
                    self.write(f"    Welcome, {student.name}.")
                    self.enrolment_menu(student.id)
                else:
                    self.write("    Invalid option.")
            except (ValueError, OSError) as error:
                self.write(f"    Error: {error}")

    def enrolment_menu(self, student_id):
        while True:
            choice = self.read(
                "        Enrolment: (c) change password, (e) enrol, "
                "(r) remove, (s) show, (x) exit: "
            ).lower()
            if choice == "x":
                return
            try:
                if choice == "e":
                    subject = self.service.enrol(student_id)
                    self.write(f"        Enrolled in subject {subject.id}.")
                elif choice == "r":
                    subject_id = self.read("        Subject ID: ")
                    self.service.remove_subject(student_id, subject_id)
                    self.write(f"        Removed subject {subject_id}.")
                elif choice == "c":
                    password = self.read("        New password: ")
                    confirmation = self.read("        Confirm password: ")
                    self.service.change_password(student_id, password, confirmation)
                    self.write("        Password changed.")
                elif choice == "s":
                    student = self.service.get_student(student_id)
                    if not student.subjects:
                        self.write("        No subjects enrolled.")
                    for subject in student.subjects:
                        self.write(f"        {subject.id}: mark {subject.mark}, grade {subject.grade}")
                    if student.average is not None:
                        self.write(f"        Average: {student.average:.2f}")
                else:
                    self.write("        Invalid option.")
            except (ValueError, OSError) as error:
                self.write(f"        Error: {error}")

    def show_students(self, students):
        if not students:
            self.write("        No students.")
        for student in students:
            average = "N/A" if student.average is None else f"{student.average:.2f}"
            self.write(f"        {student.id}: {student.name} ({student.email}) "
                       f"subjects={len(student.subjects)}, average={average}, "
                       f"grade={self.admin.grade(student)}")

    def admin_menu(self):
        while True:
            choice = self.read(
                "    Admin: (c) clear, (g) group, (p) partition, "
                "(r) remove, (s) show, (x) exit: "
            ).lower()
            if choice == "x":
                return
            try:
                if choice == "s":
                    self.show_students(self.admin.list_students())
                elif choice in ("g", "p"):
                    groups = (self.admin.group_by_grade() if choice == "g"
                              else self.admin.partition())
                    for label, students in groups.items():
                        self.write(f"    {label}:")
                        self.show_students(students)
                elif choice == "r":
                    student_id = self.read("    Student ID: ")
                    self.admin.remove(student_id)
                    self.write(f"    Removed student {student_id}.")
                elif choice == "c":
                    confirmation = self.read("    Clear all students? (y/n): ").lower()
                    if confirmation == "y":
                        self.admin.clear()
                        self.write("    Database cleared.")
                    else:
                        self.write("    Clear cancelled.")
                else:
                    self.write("    Invalid option.")
            except (ValueError, OSError) as error:
                self.write(f"    Error: {error}")
