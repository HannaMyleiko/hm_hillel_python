

"""
Student:
    id : int
    name : str
    marks : list[int]
    info : str

Features:
- fetch all students from the database
- add another yet student to the database
- retrieve the student by NAME. UI/UX issues...
"""
from __future__ import annotations

COMMANDS = ("quit", "show", "retrieve", "add")

# Simulated database

students = [ { "id": 1,
               "name": "John Doe",
               "marks": [4,5,1,4,5,2,5],
               "info": "John is 22 y.o. Hobbies: music"
              },
             { "id": 2,
               "name": "Marry Black",
               "marks": [4,1,3,4,5,1,2,2],
               "info": "Marry is 23 y.o. Hobbies: football"
               },
            ]

print(students)

# def get_avg_mark(student: str) -> float:
#     st = students["name" == student]
#     result = sum(st["marks"]) / len(st["marks"])
#     return result
#
# print (get_avg_mark("John Doe"))
def show_students () -> None:
    print("=" * 20)
    print("The list of students:\n")
    for student in students:
        print(f" ID: {student['id']}, Name: {student['name']}, Marks: {student['marks']} ")
    print("=" * 20)

def find_students (name:str) : # Return students with specified name
    result = []
    for student in students:
        if student['name'] == name:
            result.append(student)
    return result


def student_info (id: int) -> dict:
    for student in students:
        if student ["id"] == id:
            #print(f"Id: {student['id']},\n Name: {student['name']},\n Marks: {student['marks']},\n Info: {student['info']}\n ")
            return student



def student_analysis (student_list, name):
    if len(student_list) == 0:
        print(f"There is no student with name: {name}")
    elif len(student_list) == 1:
        student = student_info(student_list[0]['id'])
        print(f"Id: {student['id']},\n Name: {student['name']},\n Marks: {student['marks']},\n Info: {student['info']}\n ")
    else:
        print(f"There are {len(student_list)} wiht name {name} found:")
        for student in student_list:
            print(f" ID: {student['id']}, Name: {student['name']}, Marks: {student['marks']} ")
        id_input=input("Please, specify the student's ID: ")
        student = student_info(int(id_input))
        print(f"Id: {student['id']},\n Name: {student['name']},\n Marks: {student['marks']},\n Info: {student['info']}\n ")

def get_next_id () -> int:
    max_id = 0
    for student in students:
        if student['id'] > max_id:
            max_id = student['id']
    return max_id+1

def add_student (name: str, details: str | None):
    student_id=get_next_id()
    students.append({"id": student_id,
               "name": name,
               "marks": [],
               "info": details})





def main():
    print(f"Welcome to the Digital journal!\nAvailable commands: {COMMANDS}")
    while True:
        user_input = input("Enter the command: ")
        user_input = user_input.strip()
        if user_input not in COMMANDS:
            print(f"Command {user_input} is not available.\n")
            continue
        if user_input == "quit":
            print("See you next time.")
            break
        try:
            if user_input == "show":
                show_students()
            elif user_input == "retrieve":
                student_name = input("Input student name you are looking for:")
                requested_students=find_students(student_name)
                student_analysis(requested_students, student_name)
            elif user_input == "add":
                student_name = input("Input student name you are going to add:")
                add_student(student_name, None)


        except NotImplementedError as error:
            print(f"Feature '{error}' is not ready for live.")
        except Exception as error:
             print(error)


main()