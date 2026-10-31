class Student:
    def __init__(self, sid, name, dob):
        self.sid = sid
        self.name = name
        self.dob = dob
        self.marks = {}
        self.gpa = 0.0

    def set_mark(self, course_id, mark):
        self.marks[course_id] = mark

    def __str__(self):
        return f"{self.sid:<10} {self.name:<24} {self.dob}"
