import numpy as np


class School:
    def __init__(self):
        self.students = []
        self.courses = []

    def find_student(self, sid):
        return next((s for s in self.students if s.sid == sid), None)

    def find_course(self, cid):
        return next((c for c in self.courses if c.cid == cid), None)

    def calculate_gpa(self, student):
        ids = [cid for cid in student.marks if self.find_course(cid)]
        if not ids:
            student.gpa = 0.0
            return 0.0
        marks = np.array([student.marks[cid] for cid in ids], dtype=float)
        credits = np.array([self.find_course(cid).credits for cid in ids], dtype=float)
        student.gpa = float(np.sum(marks * credits) / np.sum(credits))
        return student.gpa

    def sort_by_gpa(self):
        if not self.students:
            return
        gpas = np.array([self.calculate_gpa(s) for s in self.students])
        order = np.argsort(-gpas, kind="stable")
        self.students = [self.students[i] for i in order]
