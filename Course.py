import pymongo
from pymongo import MongoClient
from pprint import pprint
from Department import *

course_validation = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["department_abbreviation", "course_number", "course_name", "units", "description"],
        "properties": {
            "department_abbreviation": {
                "bsonType": "string",
                "maxLength": 6,
                "description": "A reference to abbreviation from department."
            },
            "course_number": {
                "bsonType": "number",
                "minimum": 100,
                "maximum": 699,
                "description": "Digits that identifies the class offered by a department."
            },
            "course_name": {
                "bsonType": "string",
                "maxLength": 50,
                "description": "What the class is called."
            },
            "units": {
                "bsonType": "number",
                "minimum": 1,
                "maximum": 5,
                "description": "Number of credits a course offers."
            },
            "description": {
                "bsonType": "string",
                "maxLength": 80,
                "description": "A text that explains the course."
            }
        }
    }
}


def course_uniqueness(db):
    try:
        db.create_collection("courses")
    except Exception as error_message:
        pass
    db.command("collMod", "courses", validator=course_validation)
    collection = db["courses"]
    collection.create_index([("departmentAbbreviation", pymongo.ASCENDING), ("course_number", pymongo.ASCENDING)],
                            unique=True)
    collection.create_index([("departmentAbbreviation", pymongo.ASCENDING), ("course_name", pymongo.ASCENDING)],
                            unique=True)


def add_course(db):
    collection = db["courses"]
    success: bool = False

    while True:
        if success:
            break

        try:
            department = select_department(db)
            course_number = int(input("Course number--> "))
            course_name = input("Course name--> ")
            units = int(input("Units offered--> "))
            description = input("Description of course --> ")
            course = {
                "department_abbreviation": department.get("abbreviation"),
                "course_number": course_number,
                "course_name": course_name,
                "units": units,
                "description": description,
                "sections": []
            }
            new_course = collection.insert_one(course)

            filter_criteria = {"abbreviation": department.get("abbreviation")}
            update = {"$push": {"courses": course.get("_id")}}
            result = db["departments"].update_one(filter_criteria, update)

            success = True
        except Exception as error_message:
            print("The following error occurred:", error_message)
            print("Make sure the information is valid")


def list_course(db):
    courses = db["courses"].find({}).sort([("_id", pymongo.ASCENDING)])
    for course in courses:
        pprint(course)


def select_course(db):
    collection = db["courses"]
    found: bool = False
    course_number: str = ''
    department_abbreviation: str = ''

    while not found:
        department_abbreviation = input("Enter the department abbreviation the course is connected to--> ")
        course_number = int(input("Enter the course number--> "))
        course_number_count: int = collection.count_documents({"course_number": course_number,
                                                               "department_abbreviation": department_abbreviation})
        found = course_number_count == 1
        if not found:
            print("No course with that number.  Try again.")
    return_course = collection.find_one({"course_number": course_number,
                                         "department_abbreviation": department_abbreviation})
    return return_course


def delete_course(db):
    course = select_course(db)
    courses = db["courses"]
    departments = db["departments"]

    if course and "sections" in course:
        if len(course["sections"]) != 0:
            print("Can't delete this course because a section is connected to it.")
        else:
            update = departments.update_one({"abbreviation": course.get("department_abbreviation")},
                                            {"$pull": {"courses": course.get("_id")}})
        
            deleted = courses.delete_one({"_id": course["_id"]})
            print(f"We just deleted: {deleted.deleted_count} course.")
