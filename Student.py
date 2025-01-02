import pymongo
from pymongo import MongoClient
from pprint import pprint

student_validation = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["lastname", "firstname", "eMail"],
        "properties": {
            "lastname": {
                "bsonType": "string",
                "maxLength": 50,
                "description": "Last part of what a student is referred as."
            },
            "firstname": {
                "bsonType": "string",
                "maxLength": 50,
                "description": "First part of what a student is referred as."
            },
            "eMail": {
                "bsonType": "string",
                "maxLength": 80,
                "description": "An online messaging platform."
            }
        }
    }
}


def student_uniqueness(db):
    try:
        db.create_collection("students")
    except Exception as error_message:
        pass
    db.command("collMod", "students", validator=student_validation)
    collection = db["students"]
    collection.create_index([("lastname", pymongo.ASCENDING), ("firstname", pymongo.ASCENDING)],
                            unique=True)
    collection.create_index([("eMail", pymongo.ASCENDING)],
                            unique=True)


def add_student(db):
    collection = db["students"]
    success: bool = False

    while True:
        if success:
            break

        try:
            lastname = input("Last name of student--> ")
            firstname = input("First name of student --> ")
            email = input("Enter the email of student --> ")
            students = {
                "lastname": lastname,
                "firstname": firstname,
                "eMail": email,
            }
            new_major = collection.insert_one(students)

            success = True
        except Exception as error_message:
            print("The following error occurred:", error_message)
            print("Make sure the information is valid")


def list_student(db):
    students = db["students"].find({}).sort([("_id", pymongo.ASCENDING)])
    for student in students:
        pprint(student)


def select_student(db):
    collection = db["students"]
    found: bool = False
    student_last_name: str = ''
    student_first_name: str = ''

    while not found:
        student_last_name = input("Enter the students last name --> ")
        student_first_name = input("Enter the students first name --> ")
        student_name_count: int = collection.count_documents({"lastname": student_last_name,
                                                              "firstname": student_first_name})
        found = student_name_count == 1
        if not found:
            print("No student with that name.  Try again.")
    return_student = collection.find_one({"lastname": student_last_name, "firstname": student_first_name})
    return return_student


def delete_student(db):
    student = select_student(db)
    students = db["students"]

    deleted = students.delete_one({"_id": student["_id"]})
    print(f"We just deleted: {deleted.deleted_count} student.")