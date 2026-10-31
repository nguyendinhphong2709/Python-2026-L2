"""Main script: coordinates domains, input and output."""
import curses

from domains import School
from input import input_courses, input_marks, input_students
from output import UI, show_courses, show_gpa, show_marks, show_students

MENU = [
    ("1. Input students", input_students),
    ("2. Input courses", input_courses),
    ("3. Input marks", input_marks),
    ("4. List of courses", show_courses),
    ("5. List of students", show_students),
    ("6. Marks of a course", show_marks),
    ("7. GPA ranking", show_gpa),
    ("0. Exit", None),
]


def main(scr):
    ui = UI(scr)
    school = School()
    labels = [label for label, _ in MENU]
    while True:
        action = MENU[ui.menu("Student Mark Management", labels)][1]
        if action is None:
            break
        action(ui, school)


if __name__ == "__main__":
    curses.wrapper(main)
