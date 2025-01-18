import json
import csv
from csv import DictReader
from pathlib import Path

from nbformat.v4 import writes_json

files_dir = Path(__name__).absolute().parent / "files"
students_json = "students.json"
students_csv = "students.csv"

def open_json() -> dict:
    with open(files_dir / students_json) as file:
        data = json.load(file)
        # print(data)
    return data


def to_student(csv_row) -> tuple[int, str, str, str]:
    # student = {}
    name=csv_row['name']
    marks=csv_row['marks']
    info=csv_row['info']
    student_id = int(csv_row['id'])
    return student_id, name, marks, info


def to_marks(data: str) -> list[int]:
    if len(data) < 2:
        return []
    try:
        data = data[1:len(data)-1]
        marks = [int(item) for item in data.split(",")]
        return marks
    except Exception as e:
        error = f"Cannot determine marks from '{data}': {e}"
        raise Exception(error) from e



def open_csv() -> dict:
    result = {}
    with open(files_dir / students_csv, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # print(f"ROW: {row}")
            id_, name, s_marks, info = to_student(row)
            marks = to_marks(s_marks)
            result[id_] = {"name": name, "marks": marks, "info": info}
    return result

def write_csv(students: dict):
    fields = ["id","name", "marks", "info"]
    # print(f"Write students...\n {students}")
    with open(files_dir / students_csv, mode="w") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for student_id in students.keys():
            writer.writerow({"id": student_id, "name": students[student_id]['name'], "marks": students[student_id]['marks'], "info": students[student_id].get('info')})

def get_file_path(source_type: str):
    file_name = ''
    if source_type.lower() == 'json':
        file_name = students_json
    elif source_type.lower() == 'csv':
        file_name = students_csv
    else:
        print(f"Unknown file format: {source_type}")
        raise Exception(f"Unknown file format: {source_type}")

    file_path = Path(__name__).absolute().parent / "files" / file_name
    return file_path


def exists(source_type: str) ->bool:
    file_path = get_file_path(source_type)
    return file_path.exists()

def init(source_type: str, data: dict):
    # file_path: Path = get_file_path(source_type)
    if source_type.lower() == 'csv':
        write_csv(data)
    else:
        raise NotImplementedError("Only CSV is implemented")


# students = {
#     1: {
#         "name": "John Doe",
#         "marks": [4, 5, 1, 4, 5, 2, 5],
#         "info": "John is 22 y.o. Hobbies: music",
#     },
#     2: {
#         "name": "Marry Black",
#         "marks": [4, 1, 3, 4, 5, 1, 2, 2],
#         "info": "John is 23 y.o. Hobbies: football",
#     }
# }
#
# write_csv(students)
# students_read = open_csv()
# print(students_read)
# print(exists("json"))
# print(exists("csv"))
# init("csv", students)