"""Admin reporting and deletion using current saved records."""


class AdminService:
    def __init__(self, database):
        self.database = database

    def list_students(self):
        return self.database.get_all()

    @staticmethod
    def grade(student):
        average = student.average
        if average is None:
            return "NO RESULT"
        if average < 50:
            return "Z"
        if average < 65:
            return "P"
        if average < 75:
            return "C"
        if average < 85:
            return "D"
        return "HD"

    def group_by_grade(self):
        groups = {grade: [] for grade in ("Z", "P", "C", "D", "HD", "NO RESULT")}
        for student in self.list_students():
            groups[self.grade(student)].append(student)
        return groups

    def partition(self):
        groups = {result: [] for result in ("PASS", "FAIL", "INCOMPLETE")}
        for student in self.list_students():
            if len(student.subjects) < student.MAX_SUBJECTS:
                result = "INCOMPLETE"
            else:
                result = "PASS" if student.average >= 50 else "FAIL"
            groups[result].append(student)
        return groups

    def remove(self, student_id):
        self.database.remove(student_id)

    def clear(self):
        self.database.clear()
