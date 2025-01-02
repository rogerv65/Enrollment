import pymongo
from pymongo import MongoClient
from pprint import pprint
from Section import *
from Student import *

enrollment_validation = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["student_id", "section_id"],
        "properties": {
            "student_id": {
                "bsonType": "objectId",
                "description": "A reference to '_id' from Student."
            },
            "section_id": {
                "bsonType": "objectId",
                "description": "A reference to '_id' from Section."
            }
        }
    }
}


def enrollment_uniqueness(db):
    try:
        db.create_collection("enrollments")
    except Exception as error_message:
        pass
    db.command("collMod", "enrollments", validator=enrollment_validation)
    collection = db["enrollments"]

    collection.create_index([("student_id", pymongo.ASCENDING), ("section_id", pymongo.ASCENDING)], unique=True)

    collection.create_index([("semester", pymongo.ASCENDING), ("section_year", pymongo.ASCENDING),
                             ("department_abbreviation", pymongo.ASCENDING), ("course_number", pymongo.ASCENDING),
                             ("student_ID", pymongo.ASCENDING)], unique=False)


def add_student_section(db):
    student = db["students"]
    section = db["sections"]
    collection = db["enrollments"]
    success: bool = False

    while True:
        if success:
            break

        try:
            student = select_student(db)
            section = select_section(db)

            enrollment = {
                "student_id": student.get("_id"),
                "section_id": section.get("_id")
            }
            new_enrollment = collection.insert_one(enrollment)

            success = True
        except Exception as error_message:
            print("The following error occurred:", error_message)
            print("Make sure the information is valid")


def add_section_student(db):
    student = db["students"]
    section = db["sections"]
    collection = db["enrollments"]
    success: bool = False

    while True:
        if success:
            break

        try:
            section = select_section(db)
            student = select_student(db)

            enrollment = {
                "student_id": student.get("_id"),
                "section_id": section.get("_id")
            }
            new_enrollment = collection.insert_one(enrollment)

            success = True
        except Exception as error_message:
            print("The following error occurred:", error_message)
            print("Make sure the information is valid")


def list_enrollment(db):
    enrollments = db["enrollments"].find({}).sort([("student_id", pymongo.ASCENDING)])
    for enrollment in enrollments:
        pprint(enrollment)


def select_enrollment(db):
    collection = db["enrollments"]
    found: bool = False

    while not found:
        student = select_student(db)
        section = select_section(db)
        enrollment_count: int = collection.count_documents({
            "section_id": section.get("_id"),
            "student_id": student.get("_id")
        })
        found = enrollment_count == 1
        if not found:
            print("No enrollment with that student and section was found.  Try again.")
    return_enrollment = collection.find_one({"section_id": section.get("_id"),
                                             "student_id": student.get("_id")})
    return return_enrollment


def delete_student_section(db):
    student = select_student(db)
    section = select_section(db)
    enrollments = db["enrollments"]
    letter_grades = db["letter_grades"]
    pass_fails = db["pass_fails"]

    deleted2 = letter_grades.delete_one({
        "student_id": student["_id"]
    })

    deleted3 = pass_fails.delete_one({
        "student_id": student["_id"]
    })

    deleted = enrollments.delete_one({
        "section_id": section["_id"],
        "student_id": student["_id"]})

    print(f"We just un-enrolled: {deleted.deleted_count} student.")


def delete_section_student(db):
    section = select_section(db)
    student = select_student(db)
    enrollments = db["enrollments"]
    letter_grades = db["letter_grades"]
    pass_fails = db["pass_fails"]

    deleted2 = letter_grades.delete_one({
        "student_id": student["_id"]
    })

    deleted3 = pass_fails.delete_one({
        "student_id": student["_id"]
    })

    deleted = enrollments.delete_one({
        "section_id": section["_id"],
        "student_id": student["_id"]})

    print(f"We just un-enrolled: {deleted.deleted_count} section.")
