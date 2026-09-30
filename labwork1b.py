students = []
courses = []
marks = [] 

def input_student ():
    n = int(input("Enter the number of students."))
    for i in range (n):
        sid = input(f"enter the ID {i+1}:")
        Name = input(f"enter Name {i+1}")
        DoB = input(f"input DOB {i+1}")
        students.append({"SID":sid, "Name":Name, "DoB" : DoB})
def input_courses():
    n = int(input("Number of courses: "))
    for i in range(n):
        cid = input(f"  ID môn học {i+1}: ")
        cname = input(f"  Tên môn học {i+1}: ")
        courses.append({"id": cid, "name": cname})
def input_marks():
    list_courses()
    cid = input("Choose the ID subject to enter the scores")
    if not any(c["id"] == cid for c in courses):
        print("cant find this subject")
        return
    marks[cid] = {} 
    for s in students:
        m = float(input(f"the scores of {s['Names']} ({'id'}):"))
        marks[cid][s["id"]]=m

def list_courses():
    print("Danh sách môn học:")
    for c in courses:
        print(f"  {c['id']} - {c['name']}")
def list_students():
    print("List of students")
    for s in students:
        print(f"{s['id']}-{s['name']}-{s['dob']}")
def show_marks(course_id):
    if course_id not in marks:
        print("not thing")
        return
    print(f"Score: {course_id}")
    for s in students:
        mark = marks[course_id].get(s["id"], "nothing")
        print(f"  {s['name']}: {mark}")
def main():
    while True:
        print("\n--- MENU ---")
        print("1. enter student")
        print("2. enter course")
        print("3. enter score")
        print("4. list of course")
        print("5. list of student")
        print("6. score with course")
        print("0. exit")
        choice = input("choose: ")

        if choice == "1":
            input_student()
        elif choice == "2":
            input_courses()
        elif choice == "3":
            input_marks()
        elif choice == "4":
            list_courses()
        elif choice == "5":
            list_students()
        elif choice == "6":
            cid = input("ID of course to show score: ")
            show_marks(cid)
        elif choice == "0":
            break
        else:
            print("wrong.")

if __name__ == "__main__":
    main()

