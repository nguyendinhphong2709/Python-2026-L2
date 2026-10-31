import curses
import os
import zipfile

from input import DATA_FILE, TEXT_FILES


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
        self.scr.addstr(0, 2, f"== {title} =="[: curses.COLS - 4])
        self.scr.attroff(curses.color_pair(1) | curses.A_BOLD)
        self.scr.hline(1, 0, curses.ACS_HLINE, curses.COLS - 1)
        return 3

    def line(self, y, text, pair=0, bold=False):
        if y >= curses.LINES - 1:
            return
        attr = curses.color_pair(pair) | (curses.A_BOLD if bold else 0)
        self.scr.addstr(y, 2, str(text)[: curses.COLS - 4], attr)

    def wait(self, y):
        self.line(min(y, curses.LINES - 2), "Press any key to continue...", 3)
        self.scr.getch()

    def menu(self, title, items):
        cur = 0
        while True:
            y = self.screen(title)
            for i, text in enumerate(items):
                attr = curses.color_pair(2) if i == cur else 0
                self.line(y + i, f" {text} ".ljust(40), 0)
                if i == cur:
                    self.scr.chgat(y + i, 2, min(42, curses.COLS - 4), attr)
            self.line(y + len(items) + 1, "UP/DOWN to move, ENTER to select", 3)
            k = self.scr.getch()
            if k == curses.KEY_UP:
                cur = (cur - 1) % len(items)
            elif k == curses.KEY_DOWN:
                cur = (cur + 1) % len(items)
            elif k in (curses.KEY_ENTER, 10, 13):
                return cur


def list_courses(ui, school, y):
    for i, c in enumerate(school.courses):
        ui.line(y + i, f"{c.cid} - {c.name}")
    return y + len(school.courses)


def show_students(ui, school):
    y = ui.screen("Students")
    if not school.students:
        ui.line(y, "No students yet.", 4)
    for i, s in enumerate(school.students):
        ui.line(y + i, s)
    ui.wait(y + len(school.students) + 1)


def show_courses(ui, school):
    y = ui.screen("Courses")
    if not school.courses:
        ui.line(y, "No courses yet.", 4)
    for i, c in enumerate(school.courses):
        ui.line(y + i, c)
    ui.wait(y + len(school.courses) + 1)


def show_marks(ui, school):
    from input import ask

    y = ui.screen("Show marks of a course")
    y = list_courses(ui, school, y)
    cid = ask(ui, y + 1, "ID of course to show score:")
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


def compress_data():
    files = [p for p in TEXT_FILES if os.path.exists(p)]
    if not files:
        return
    with zipfile.ZipFile(DATA_FILE, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for path in files:
            z.write(path, arcname=os.path.basename(path))
    for path in files:
        os.remove(path)
