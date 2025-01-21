"""
Student:
    name: str
    marks: list[int]

Features:
- fetch all students from the database
- add another yet student to the database
- retrieve the student by NAME. UI/UX issues...
"""
from __future__ import annotations
import files

# ==================================================
# Simulated storage
# ==================================================

students = {
    1: {
        "name": "John Doe",
        "marks": [4, 5, 1, 4, 5, 2, 5],
        "info": "John is 22 y.o. Hobbies: music",
    },
    2: {
        "name": "Marry Black",
        "marks": [4, 1, 3, 4, 5, 1, 2, 2],
        "info": "John is 23 y.o. Hobbies: football",
    }
}

LAST_ID_CONTEXT = 2
TEMPLATE_ADD = "'John Doe;4,5,4,5,4,5'"
TEMPLATE_CHANGE = "'John Doe;4,5,4,5,4,5[+]'"
TEMPLATE = TEMPLATE_ADD

def get_next_id() -> int:
    global LAST_ID_CONTEXT
    LAST_ID_CONTEXT += 1
    return LAST_ID_CONTEXT

def represent_students():
    for id_, student in students.items():
        print(f" [{id_}] {student['name']}, marks: {student['marks']}")
# ==================================================
# CRUD (Create Read Update Delete)
# ==================================================


def add_student(student : dict) -> dict|None:
    if len(student) != 2:
        return None
    elif not student.get("name") or not student.get("marks"):
        return None
    else:
        new_student_id = get_next_id()
        students[new_student_id] = student
    print(f"The student {student['name']} has been added with ID={new_student_id}")
    return student

def search_student(id_ : int):
    return students.get(id_)


def delete_student(id_ : int, student: dict):
    del students[id_]
    print(f"The student {student['name']} (ID: {id_}) has been successfully deleted")

def update_student(id_, update_data: str) -> dict:
    """ 
    Updates student by ID according to provided data 
    id_: student's ID
    update_data: data for update in the following template [<student-name>;][<marks>][+]
                 if a field is not specified the corresponding attribute is not being updated
                 if '+' is specified at the end of marks list, the marks are being appended to the existing ones
    """
    name, marks, append_marks = parse(update_data)
    # parse() may return 'None' for name and/or marks
    # append_marks (True/False) determine if provided marks should be added to the existing list
    student = students[id_]
    if name is not None:
        student['name'] = name
    if marks is not None:
        if append_marks:
            student['marks'] += marks
        else:
            student['marks'] = marks
    students[id_] = student
    return student

# ==================================================
# Handle user input
# ==================================================
def convert_to_marks(data) -> list[int] | None:
    if len(data) == 0:
        return []
    try:
        marks = [int(item) for item in data.split(",")]
        return marks
    except Exception as e:
        error = f"Cannot determine marks from '{data}': {e}"
        raise Exception(error) from e


def parse(data: str) -> tuple[str|None, list[int]|None, bool]:
    """Return student name and marks.

    user input template:
    'John Doe;4,5,4,5,4,5[+]'

    """
    add_marks = False # flag defining if marks should be added to the existing ones
    if len(data) == 0:
        raise Exception(f"Incorrect data. Template: {TEMPLATE}")
    if data[len(data)-1] == '+':
        # if '+' is at the end of data marks will be added to the existing ones
        add_marks = True
        data = data[0:len(data)-1] # trim the '+' sign from the end of the marks string
    items=data.split(";")
    if len(items) > 2:
        raise Exception(f"Incorrect data. Template: {TEMPLATE}")
    if len(items) == 2: # name and marks are specified
        name = items[0]
        marks_data = items[1]
        new_marks = convert_to_marks(marks_data)
    else: # only 'name' or 'marks' is specified
        try: # try to resolve it as marks (convert it to list[int])
            name = None
            new_marks = convert_to_marks(items[0])
        except Exception: # no luck; treat it as name
            name = items[0]
            new_marks = None
    return name, new_marks, add_marks

def ask_student_payload() -> dict:
    """
      Input template:
          'John Doe;4,5,4,5,4,5'

      Expected:
          John Doe:       str
          4,5,4,5,4,5:    list[int]
      """

    prompt = f"Enter student's payload using next template:\n{TEMPLATE}: "

    if not (payload := parse(input(prompt))):
        return None
    else:
        name, marks, _ = payload
    if name is None:
        return None
    if marks is None:
        marks = []
    return {"name": name, "marks": marks}

def find_students(name:str) : # Return students with specified name
    result = {}
    for id_, student in students.items():
        if student['name'] == name:
            result[id_] = student
    return result

def student_info(id_: int) -> dict | None:
    """ returns student by ID"""
    # print(f"Try to get Student by ID={id_}")
    student = students[id_]
    if student is None:
        print(f"There is no student with ID={id_}")
    # print(student)
    return student

def student_analysis(student_set, name) -> tuple[int, dict] | None:
    """
    Analyzes the set of students
    Returns:
     - None if there are no students
     - student: dict with specified name.
     If there are more than one student with specified name the another prompt for ID is shown
    """
    print(student_set.items())
    student_id, student=None, None
    if len(student_set) == 0:
        print(f"There is no student with name: {name}")
    elif len(student_set.keys()) == 1:
        for student_id, student in student_set.items():
            pass
    else:
        print(f"There are {len(student_set.keys())} wiht name {name} found:")
        for id_, student in student_set.items():
            print(f" ID: {id_}, Name: {student['name']}, Marks: {student['marks']} ")
        id_input=input("Please, specify the student's ID: ")
        student_id = int(id_input)
        student = student_info(student_id)

    return student_id, student

def find_student(input_data:str) -> tuple[int, dict] | None:
    student = None
    id_ = None
    try:
        id_ = int(input_data)
        student = student_info(id_)
    except Exception as e:
        print(f"{input_data} is not ID: {e}")
    if student is None:
        requested_students = find_students(input_data)
        id_, student = student_analysis(requested_students, input_data)
    return id_, student

def handle_management_command(command: str):
    global TEMPLATE
    if command == "show":
        print("Available students:")
        represent_students()
    elif command == "add":
        TEMPLATE = TEMPLATE_ADD
        data = ask_student_payload()
        if data is None:
            return None
        else:
            if not (add_student(data)):
                print(f"Can't create user with data: {data}")
    elif command == "retrieve":
        student_name = input("Input student's name or ID you are looking for:")
        id_, student = find_student(student_name)
        if student is None:
            print(f"There are no students with name/ID '{student_name}'")
        else:
            print(f"Id: {id_},\n "
                  f"Name: {student.get('name')},\n "
                  f"Marks: {student.get('marks')},\n "
                  f"Info: {student.get('info')}\n ")
    elif command == "remove":
        student_name = input("Input student's name or ID you want to remove:")
        id_, student = find_student(student_name)
        if student is None:
            print(f"There are no students with name/ID '{student_name}'")
        else:
            confirm = input(f"Are you sure you want to permanently delete the student {student['name']} (ID: {id_}) from the journal [y/n]?")
            if len(confirm)>0 and confirm.lower()[0] == 'y':
                delete_student(id_, student)
            else:
                print(f"The student {student['name']} (ID: {id_}) has not been deleted (NO confirmation)")
    elif command == "change":
        TEMPLATE = TEMPLATE_CHANGE
        student_name = input("Input student's name or ID you are going to update:")
        id_, student = find_student(student_name)
        if student is None:
            print(f"There are no students with name/ID '{student_name}'")
        else:
            update_data = input(f"Please, enter updated data for student {student['name']} (ID:{id_}).\n"
                                f"Use the following template: {TEMPLATE}.\n"
                                f"Use '+' (plus sign) to add marks instead of replace:\n")
            student = update_student(id_, update_data)
            print(f"The student {student['name']} (ID: {id_}) has been successfully updated.")
    else:
        raise SystemExit(f"Unrecognized command: '{command}'")
    files.write_csv(students)

def handle_user_input():
    """This is an application entrypoint."""
    SYSTEM_COMMANDS = ("quit", "help")
    MANAGEMENT_COMMANDS = ("show", "add", "retrieve", "remove", "change")
    AVAILABLE_COMMANDS = SYSTEM_COMMANDS + MANAGEMENT_COMMANDS

    help_message = (
        "Welcome to the Journal application. Use the menu to interact with the application.\n"
        f"Available commands: {AVAILABLE_COMMANDS}"
    )
    print(help_message)

    while True:
        try:
            command = input("Enter the command: ")
            if command  == "quit":
                print("Thank you for using the Journal application. Bye")
                break
            elif command == "help":
                print(f"{help_message}")
            elif command in MANAGEMENT_COMMANDS:
                handle_management_command(command)
            else:
                print(f"Unrecognized command '{command}'")
        except Exception as error:
            print(error)
            continue

def init(init_data):
    if not files.exists("csv"):
        files.init("csv", init_data)
    result = files.open_csv()
    return result

students = init(students)

# print(f"Students: {students}")
handle_user_input()