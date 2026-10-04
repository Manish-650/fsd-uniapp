"""Student terminal interface. Admin menus are the next development stage."""

from uniapp.services.student_service import StudentService


class CLIUniApp:
    def __init__(self, database, read=input, write=print):
        self.service = StudentService(database)
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
                    self.write("Admin functions are not implemented yet.")
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
