import curses
import math
import os
import zipfile

from domains import Course, Student

MIN_MARK, MAX_MARK = 0, 20

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
STUDENTS_FILE = os.path.join(DATA_DIR, "students.txt")
COURSES_FILE = os.path.join(DATA_DIR, "courses.txt")
MARKS_FILE = os.path.join(DATA_DIR, "marks.txt")
DATA_FILE = os.path.join(DATA_DIR, "students.dat")
TEXT_FILES = [STUDENTS_FILE, COURSES_FILE, MARKS_FILE]


def write_students(school):
    with open(STUDENTS_FILE, "w", encoding="utf-8") as f:
        for s in school.students:
            f.write(f"{s.sid},{s.name},{s.dob}\n")


def write_courses(school):
    with open(COURSES_FILE, "w", encoding="utf-8") as f:
        for c in school.courses:
            f.write(f"{c.cid},{c.name},{c.credits}\n")


def write_marks(school):
    with open(MARKS_FILE, "w", encoding="utf-8") as f:
        for s in school.students:
            for cid, mark in s.marks.items():
                f.write(f"{s.sid},{cid},{mark}\n")


def round_down(x):
    return math.floor(x * 10 + 1e-9) / 10


def ask(ui, y, prompt):
    ui.line(y, prompt, 5)
    curses.echo()
    curses.curs_set(1)
    ui.scr.move(y, 2 + len(prompt) + 1)
    ui.scr.clrtoeol()
    text = ui.scr.getstr().decode("utf-8", errors="ignore").strip()
    curses.noecho()
    curses.curs_set(0)
    return text


def ask_int(ui, y, prompt, minimum=0):
    while True:
        try:
            v = int(ask(ui, y, prompt))
            if v >= minimum:
                return v
        except ValueError:
            pass
        ui.line(y + 1, f"Invalid number (>= {minimum}), try again.", 4)


def ask_float(ui, y, prompt, lo, hi):
    while True:
        try:
            v = float(ask(ui, y, prompt))
            if lo <= v <= hi:
                return v
        except ValueError:
            pass
        ui.line(y + 1, f"Invalid mark ({lo}-{hi}), try again.", 4)


def ask_unique(ui, y, prompt, exists):
    while True:
        v = ask(ui, y, prompt)
        if v and not exists(v):
            return v
        ui.line(y + 1, "Empty or duplicate ID, try again.", 4)


def input_students(ui, school):
    y = ui.screen("Input students")
    n = ask_int(ui, y, "Number of students:", 1)
    for i in range(n):
        y = ui.screen(f"Input student {i + 1}/{n}")
        sid = ask_unique(ui, y, "ID:", school.find_student)
        ui.line(y + 1, " " * 40)
        name = ask(ui, y + 2, "Name:")
        dob = ask(ui, y + 3, "DoB (dd/mm/yyyy):")
        school.students.append(Student(sid, name, dob))
    write_students(school)


def input_courses(ui, school):
    y = ui.screen("Input courses")
    n = ask_int(ui, y, "Number of courses:", 1)
    for i in range(n):
        y = ui.screen(f"Input course {i + 1}/{n}")
        cid = ask_unique(ui, y, "ID:", school.find_course)
        ui.line(y + 1, " " * 40)
        name = ask(ui, y + 2, "Name:")
        credits = ask_int(ui, y + 3, "Credits:", 1)
        school.courses.append(Course(cid, name, credits))
    write_courses(school)


def input_marks(ui, school):
    from output import list_courses

    y = ui.screen("Input marks")
    if not school.students or not school.courses:
        ui.line(y, "Need students and courses first.", 4)
        return ui.wait(y + 2)
    y = list_courses(ui, school, y)
    cid = ask(ui, y + 1, "Choose the ID subject to enter the scores:")
    course = school.find_course(cid)
    if course is None:
        ui.line(y + 3, "Can't find this subject.", 4)
        return ui.wait(y + 5)
    for s in school.students:
        y = ui.screen(f"Marks for {course.name}")
        raw = ask_float(ui, y, f"Mark of {s.name} ({s.sid}):", MIN_MARK, MAX_MARK)
        s.set_mark(course.cid, round_down(raw))
    write_marks(school)


def read_lines(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f if line.strip()]


def load_data(school):
    if not os.path.exists(DATA_FILE):
        return False
    with zipfile.ZipFile(DATA_FILE) as z:
        names = z.namelist()
        for path in TEXT_FILES:
            name = os.path.basename(path)
            if name in names:
                with open(path, "wb") as f:
                    f.write(z.read(name))
    for line in read_lines(STUDENTS_FILE):
        sid, rest = line.split(",", 1)
        name, dob = rest.rsplit(",", 1)
        school.students.append(Student(sid, name, dob))
    for line in read_lines(COURSES_FILE):
        cid, rest = line.split(",", 1)
        name, credits = rest.rsplit(",", 1)
        school.courses.append(Course(cid, name, int(credits)))
    for line in read_lines(MARKS_FILE):
        sid, cid, mark = line.split(",")
        student = school.find_student(sid)
        if student:
            student.set_mark(cid, float(mark))
    return True
