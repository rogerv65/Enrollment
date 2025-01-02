import pymongo
from pymongo import MongoClient
from pprint import pprint
from Major import *
from Student import *

student_major_validation = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["major_name", "last_name", "first_name"],
        "properties": {
            "major_name": {
                "bsonType": "string",
                "maxLength": 50,
                "description": "What the major is called."
            },
            "last_name": {
                "bsonType": "string",
                "maxLength": 50,
                "description": "Last part of what a student is referred as."
            },
            "first_name": {
                "bsonType": "string",
                "maxLength": 50,
                "description": "First part of what a student is referred as."
            }
        }
    }
}


def student_major_uniqueness(db):
    try:
        db.create_collection("student_majors")
    except Exception as error_message:
        pass
    db.command("collMod", "student_majors", validator=student_major_validation)
    collection = db["student_majors"]

    collection.create_index([("major_name", pymongo.ASCENDING), ("last_name", pymongo.ASCENDING),
                             ("first_name", pymongo.ASCENDING)], unique=True)


def add_student_major(db):
    collection = db["student_majors"]
    success: bool = False

    while True:
        if success:
            break

        try:
            student = select_student(db)
            major = select_major(db)

            student_major = {
                "major_name": major.get("name"),
                "last_name": student.get("lastname"),
                "first_name": student.get("firstname")
            }
            new_student_major = collection.insert_one(student_major)

            success = True
        except Exception as error_message:
            print("The following error occurred:", error_message)
            print("Make sure the information is valid")


def add_major_student(db):
    collection = db["student_majors"]
    success: bool = False

    while True:
        if success:
            break

        try:
            major = select_major(db)
            student = select_student(db)

            student_major = {
                "major_name": major.get("name"),
                "last_name": student.get("lastname"),
                "first_name": student.get("firstname")
            }
            new_student_major = collection.insert_one(student_major)

            success = True
        except Exception as error_message:
            print("The following error occurred:", error_message)
            print("Make sure the information is valid")


def list_student_major(db):
    student_majors = db["student_majors"].find({}).sort([("major_name", pymongo.ASCENDING)])
    for student_major in student_majors:
        pprint(student_major)


def delete_student_major(db):
    student = select_student(db)
    major = select_major(db)
    student_majors = db["student_majors"]

    deleted = student_majors.delete_one({"last_name": student["lastname"],
                                         "first_name": student["firstname"],
                                         "major_name": major["name"]})
    print(f"We just removed: {deleted.deleted_count} student.")


def delete_major_student(db):
    student = select_student(db)
    major = select_major(db)
    student_majors = db["student_majors"]

    deleted = student_majors.delete_one({"major_name": major["name"],
                                         "last_name": student["lastname"],
                                         "first_name": student["firstname"]})
    print(f"We just removed: {deleted.deleted_count} major.")
