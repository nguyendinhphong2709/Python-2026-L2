class Entity:
    def __init__(self):
        self._id = ""
        self._name = ""

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def input(self):
        raise NotImplementedError

    def list(self):
        raise NotImplementedError


class Student(Entity):
    def __init__(self):
        super().__init__()
        self.__dob = ""

    def get_dob(self):
        return self.__dob

    def input(self):
        self._id = input("  Student ID: ").strip()
        self._name = input("  Student name: ").strip()
        self.__dob = input("  Date of birth (dd/mm/yyyy): ").strip()

    def list(self):
        print(f"  {self._id:<10} {self._name:<25} {self.__dob}")


class Course(Entity):
    def __init__(self):
        super().__init__()
        self.__marks = {}

    def input(self):
        self._id = input("  Course ID: ").strip()
        self._name = input("  Course name: ").strip()

    def list(self):
        print(f"  {self._id:<10} {self._name}")

    def set_mark(self, student_id, mark):
        if mark < 0 or mark > 20:
            raise ValueError("Mark must be between 0 and 20")
        self.__marks[student_id] = mark

    def get_mark(self, student_id):
        return self.__marks.get(student_id)


class School:
    def __init__(self):
        self.__students = []
        self.__courses = []

    @staticmethod
    def __input_positive_int(prompt):
        while True:
            try:
                n = int(input(prompt))
                if n > 0:
                    return n
            except ValueError:
                pass
            print("  Please enter a positive integer.")

    def __input_entities(self, cls, target, label):
        n = self.__input_positive_int(f"Number of {label}s: ")
        for i in range(n):
            print(f"{label.capitalize()} #{i + 1}")
            e = cls()
            e.input()
            target.append(e)

    def input_students(self):
        self.__input_entities(Student, self.__students, "student")

    def input_courses(self):
        self.__input_entities(Course, self.__courses, "course")

    def __find_course(self):
        if not self.__courses:
            print("No courses yet.")
            return None
        self.list_courses()
        cid = input("Select course ID: ").strip()
        for c in self.__courses:
            if c.get_id() == cid:
                return c
        print("Course not found.")
        return None

    def input_marks(self):
        if not self.__students:
            print("No students yet.")
            return
        course = self.__find_course()
        if course is None:
            return
        for s in self.__students:
            while True:
                try:
                    mark = float(input(f"  Mark of {s.get_name()} ({s.get_id()}): "))
                    course.set_mark(s.get_id(), mark)
                    break
                except ValueError as e:
                    print(" ", e if str(e).startswith("Mark") else "Invalid number.")

    def list_students(self):
        print("Students:")
        for s in self.__students:
            s.list()

    def list_courses(self):
        print("Courses:")
        for c in self.__courses:
            c.list()

    def show_marks(self):
        course = self.__find_course()
        if course is None:
            return
        print(f"Marks for {course.get_name()}:")
        for s in self.__students:
            mark = course.get_mark(s.get_id())
            print(f"  {s.get_id():<10} {s.get_name():<25} {'-' if mark is None else mark}")

    def run(self):
        actions = {
            "1": self.input_students,
            "2": self.input_courses,
            "3": self.input_marks,
            "4": self.list_students,
            "5": self.list_courses,
            "6": self.show_marks,
        }
        while True:
            print("\n1. Input students\n2. Input courses\n3. Input marks for a course")
            print("4. List students\n5. List courses\n6. Show marks for a course\n0. Exit")
            choice = input("Choose: ").strip()
            if choice == "0":
                break
            action = actions.get(choice)
            if action:
                action()
            else:
                print("Invalid choice.")


if __name__ == "__main__":
    School().run()
