"""Tkinter interface for already registered students."""

import tkinter as tk
from tkinter import ttk

from uniapp.services.student_service import StudentService


class GUIUniApp:
    def __init__(self, root, database):
        self.root = root
        self.service = StudentService(database)
        self.student_id = None
        self.enrolment_window = None
        self.subject_window = None
        self.error_window = None
        root.title("UniApp - Student Login")
        root.minsize(420, 240)
        frame = ttk.Frame(root, padding=24)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="Student Login", font=("Arial", 18)).pack(pady=(0, 12))
        ttk.Label(frame, text="Email").pack(anchor="w")
        self.email = ttk.Entry(frame, width=42)
        self.email.pack(fill="x", pady=(0, 8))
        ttk.Label(frame, text="Password").pack(anchor="w")
        self.password = ttk.Entry(frame, show="*", width=42)
        self.password.pack(fill="x", pady=(0, 12))
        ttk.Button(frame, text="Log in", command=self.login).pack()
        ttk.Label(frame, text="Register through the terminal app first.").pack(pady=10)
        root.bind("<Return>", lambda event: self.login())
        self.email.focus_set()

    def show_error(self, message):
        if self.error_window is not None and self.error_window.winfo_exists():
            self.error_window.destroy()
        parent = self.enrolment_window if self.student_id is not None else self.root
        window = tk.Toplevel(parent)
        self.error_window = window
        window.title("UniApp - Error")
        window.transient(parent)
        frame = ttk.Frame(window, padding=20)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text=str(message), wraplength=360).pack(pady=(0, 15))
        ttk.Button(frame, text="OK", command=window.destroy).pack()
        window.grab_set()
        window.bind("<Return>", lambda event: window.destroy())
        window.bind("<Escape>", lambda event: window.destroy())

    def login(self):
        if self.student_id is not None:
            return
        try:
            if not self.email.get().strip() or not self.password.get().strip():
                raise ValueError("Email and password are required.")
            student = self.service.login(self.email.get(), self.password.get())
        except (ValueError, OSError) as error:
            self.show_error(error)
            return
        self.student_id = student.id
        self.password.delete(0, tk.END)
        self.root.withdraw()
        window = tk.Toplevel(self.root)
        self.enrolment_window = window
        window.title("UniApp - Enrolment")
        window.minsize(420, 230)
        window.protocol("WM_DELETE_WINDOW", self.logout)
        frame = ttk.Frame(window, padding=24)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text=f"Welcome, {student.name}", font=("Arial", 16)).pack(pady=8)
        self.status = tk.StringVar(value=f"Subjects enrolled: {len(student.subjects)}/4")
        ttk.Label(frame, textvariable=self.status).pack(pady=8)
        ttk.Button(frame, text="Enrol in a subject", command=self.enrol).pack(fill="x", pady=4)
        ttk.Button(frame, text="Show subjects", command=self.show_subjects).pack(fill="x", pady=4)
        ttk.Button(frame, text="Log out", command=self.logout).pack(pady=8)

    def enrol(self):
        if self.student_id is None:
            return
        try:
            subject = self.service.enrol(self.student_id)
            student = self.service.get_student(self.student_id)
            self.status.set(f"Enrolled {subject.id}. Subjects enrolled: {len(student.subjects)}/4")
            if self.subject_window is not None and self.subject_window.winfo_exists():
                self.refresh_subjects(student)
        except (ValueError, OSError) as error:
            self.show_error(error)

    def show_subjects(self):
        if self.student_id is None:
            return
        try:
            student = self.service.get_student(self.student_id)
        except (ValueError, OSError) as error:
            self.show_error(error)
            return
        if self.subject_window is None or not self.subject_window.winfo_exists():
            window = tk.Toplevel(self.enrolment_window)
            self.subject_window = window
            window.title("UniApp - Subjects")
            frame = ttk.Frame(window, padding=20)
            frame.pack(fill="both", expand=True)
            self.table = ttk.Treeview(frame, columns=("id", "mark", "grade"),
                                      show="headings", height=4)
            for column, heading in (("id", "Subject ID"), ("mark", "Mark"), ("grade", "Grade")):
                self.table.heading(column, text=heading)
                self.table.column(column, width=110, anchor="center")
            self.table.pack(fill="both", expand=True)
            self.average = tk.StringVar()
            ttk.Label(frame, textvariable=self.average).pack(pady=10)
            ttk.Button(frame, text="Refresh", command=self.show_subjects).pack()
        self.refresh_subjects(student)
        self.subject_window.lift()

    def refresh_subjects(self, student):
        for item in self.table.get_children():
            self.table.delete(item)
        for subject in student.subjects:
            self.table.insert("", "end", values=(subject.id, subject.mark, subject.grade))
        value = "No subjects enrolled." if student.average is None else f"Average: {student.average:.2f}"
        self.average.set(value)

    def logout(self):
        # Destroy child windows too, so the next account cannot see old results.
        if self.enrolment_window is not None:
            self.enrolment_window.destroy()
        self.enrolment_window = self.subject_window = self.error_window = None
        self.student_id = None
        self.password.delete(0, tk.END)
        self.root.deiconify()
        self.email.focus_set()
