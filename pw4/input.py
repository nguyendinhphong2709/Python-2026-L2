"""Input functions: read data from the keyboard via curses."""
import curses
import math

from domains import Course, Student

MIN_MARK, MAX_MARK = 0, 20


def round_down(x):
    """Round down to 1 decimal place using math.floor()."""
    return math.floor(x * 10 + 1e-9) / 10


def ask(ui, y, prompt):
    ui.line(y, prompt, 5)
    curses.echo()
    curses.curs_set(1)
    ui.scr.move(y, 2 + len(prompt) + 1)
    ui.scr.clrtoeol()  # clear leftover text from a previous attempt
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
