import curses
import math

import numpy as np


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


class Course:
    def __init__(self, cid, name, credits):
        self.cid = cid
        self.name = name
        self.credits = credits

    def __str__(self):
        return f"{self.cid:<10} {self.name:<24} {self.credits} credits"


class School:
    def __init__(self):
        self.students = []
        self.courses = []

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
        for s in self.students:
            self.calculate_gpa(s)
        self.students.sort(key=lambda s: s.gpa, reverse=True)


def round_down(x):
    return math.floor(x * 10 + 1e-9) / 10


class UI:
    def __init__(self, scr):
        self.scr = scr
        curses.curs_set(0)
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_CYAN, -1)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(3, curses.COLOR_GREEN, -1)
        curses.init_pair(4, curses.COLOR_RED, -1)
        curses.init_pair(5, curses.COLOR_YELLOW, -1)

    def screen(self, title):
        self.scr.clear()
        self.scr.attron(curses.color_pair(1) | curses.A_BOLD)
        self.scr.addstr(0, 2, f"== {title} ==")
        self.scr.attroff(curses.color_pair(1) | curses.A_BOLD)
        self.scr.hline(1, 0, curses.ACS_HLINE, curses.COLS - 1)
        return 3

    def line(self, y, text, pair=0, bold=False):
        attr = curses.color_pair(pair) | (curses.A_BOLD if bold else 0)
        self.scr.addstr(y, 2, str(text)[: curses.COLS - 4], attr)

    def ask(self, y, prompt):
        self.line(y, prompt, 5)
        curses.echo()
        curses.curs_set(1)
        self.scr.move(y, 2 + len(prompt) + 1)
        text = self.scr.getstr().decode("utf-8").strip()
        curses.noecho()
        curses.curs_set(0)
        return text

    def ask_int(self, y, prompt, minimum=0):
        while True:
            try:
                v = int(self.ask(y, prompt))
                if v >= minimum:
                    return v
            except ValueError:
                pass
            self.line(y + 1, "Invalid number, try again.", 4)

    def ask_float(self, y, prompt):
        while True:
            try:
                return float(self.ask(y, prompt))
            except ValueError:
                self.line(y + 1, "Invalid number, try again.", 4)

    def wait(self, y):
        self.line(y, "Press any key to continue...", 3)
        self.scr.getch()

    def menu(self, title, items):
        cur = 0
        while True:
            y = self.screen(title)
            for i, text in enumerate(items):
                attr = curses.color_pair(2) if i == cur else 0
                self.scr.addstr(y + i, 4, f" {text} ".ljust(40), attr)
            self.line(y + len(items) + 1, "UP/DOWN to move, ENTER to select", 3)
            k = self.scr.getch()
            if k == curses.KEY_UP:
                cur = (cur - 1) % len(items)
            elif k == curses.KEY_DOWN:
                cur = (cur + 1) % len(items)
            elif k in (curses.KEY_ENTER, 10, 13):
                return cur


def input_students(ui, school):
    y = ui.screen("Input students")
    n = ui.ask_int(y, "Number of students:", 1)
    for i in range(n):
        y = ui.screen(f"Input student {i + 1}/{n}")
        sid = ui.ask(y, "ID:")
        name = ui.ask(y + 1, "Name:")
        dob = ui.ask(y + 2, "DoB (dd/mm/yyyy):")
        school.students.append(Student(sid, name, dob))


def input_courses(ui, school):
    y = ui.screen("Input courses")
    n = ui.ask_int(y, "Number of courses:", 1)
    for i in range(n):
        y = ui.screen(f"Input course {i + 1}/{n}")
        cid = ui.ask(y, "ID:")
        name = ui.ask(y + 1, "Name:")
        credits = ui.ask_int(y + 2, "Credits:", 1)
        school.courses.append(Course(cid, name, credits))


def input_marks(ui, school):
    y = ui.screen("Input marks")
    if not school.students or not school.courses:
        ui.line(y, "Need students and courses first.", 4)
        return ui.wait(y + 2)
    for i, c in enumerate(school.courses):
        ui.line(y + i, f"{c.cid} - {c.name}")
    cid = ui.ask(y + len(school.courses) + 1, "Choose the ID subject to enter the scores:")
    course = school.find_course(cid)
    if course is None:
        ui.line(y + len(school.courses) + 3, "Can't find this subject.", 4)
        return ui.wait(y + len(school.courses) + 5)
    for s in school.students:
        y = ui.screen(f"Marks for {course.name}")
        raw = ui.ask_float(y, f"Mark of {s.name} ({s.sid}):")
        s.set_mark(course.cid, round_down(raw))


def show_students(ui, school):
    y = ui.screen("Students")
    for i, s in enumerate(school.students):
        ui.line(y + i, s)
    ui.wait(y + len(school.students) + 1)


def show_courses(ui, school):
    y = ui.screen("Courses")
    for i, c in enumerate(school.courses):
        ui.line(y + i, c)
    ui.wait(y + len(school.courses) + 1)


def show_marks(ui, school):
    y = ui.screen("Show marks of a course")
    for i, c in enumerate(school.courses):
        ui.line(y + i, f"{c.cid} - {c.name}")
    cid = ui.ask(y + len(school.courses) + 1, "ID of course to show score:")
    course = school.find_course(cid)
    y = ui.screen("Marks")
    if course is None:
        ui.line(y, "Can't find this subject.", 4)
        return ui.wait(y + 2)
    ui.line(y, f"{course.name} ({course.credits} credits)", 5, True)
    for i, s in enumerate(school.students):
        m = s.marks.get(course.cid)
        ui.line(y + 1 + i, f"{s.sid:<10} {s.name:<24} {m if m is not None else 'N/A'}")
    ui.wait(y + len(school.students) + 2)


def show_gpa(ui, school):
    school.sort_by_gpa()
    y = ui.screen("GPA ranking (descending)")
    ui.line(y, f"{'Rank':<6}{'ID':<10} {'Name':<24} GPA", 5, True)
    for i, s in enumerate(school.students):
        ui.line(y + 1 + i, f"{i + 1:<6}{s.sid:<10} {s.name:<24} {s.gpa:.2f}")
    ui.wait(y + len(school.students) + 2)


def main(scr):
    ui = UI(scr)
    school = School()
    items = [
        "1. Input students",
        "2. Input courses",
        "3. Input marks",
        "4. List of courses",
        "5. List of students",
        "6. Marks of a course",
        "7. GPA ranking",
        "0. Exit",
    ]
    actions = [input_students, input_courses, input_marks,
               show_courses, show_students, show_marks, show_gpa]
    while True:
        choice = ui.menu("Student Mark Management", items)
        if choice == len(items) - 1:
            break
        actions[choice](ui, school)


if __name__ == "__main__":
    curses.wrapper(main)
