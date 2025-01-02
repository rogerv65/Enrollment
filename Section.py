import pymongo
from pymongo import MongoClient
from pprint import pprint
from Course import *

section_validation = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["department_abbreviation", "course_number",
                     "section_number", "semester", "section_year", "building",
                     "room", "schedule", "start_time", "instructor"],
        "properties": {
            "department_abbreviation": {
                "bsonType": "string",
                "maxLength": 6,
                "description": "A reference to 'department_abbreviation' in course."
            },
            "course_number": {
                "bsonType": "number",
                "minimum": 100,
                "maximum": 699,
                "description": "A reference to 'course_number' found in course."
            },
            "section_number": {
                "bsonType": "number",
                "description": "Digits that identifies the section that is offered by a class."
            },
            "semester": {
                "enum": ['Fall', 'Spring', 'Summer I', 'Summer II', 'Summer III', 'Winter'],
                "description": "The name of the half-year term that section is offered."
            },
            "section_year": {
                "bsonType": "number",
                "description": "Number that identifies the year a section is taken."
            },
            "building": {
                "enum": ['ANAC', 'CDC', 'DC', 'ECS', 'EN2', 'EN3', 'EN4', 'EN5', 'ET', 'HSCI', 'NUR', 'VEC'],
                "description": "The structure that the section is located in."
            },
            "room": {
                "bsonType": "number",
                "minimum": 1,
                "maximum": 999,
                "description": "Number that identifies the location a section takes place in."
            },
            "schedule": {
                "enum": ['MW', 'TuTh', 'MWF', 'F', 'S'],
                "description": "The day that a section takes place."
            },
            "start_time": {
                "bsonType": "string",
                "maxLength": 10,
                "description": "Identifies the hour and minute a section begins."
            },
            "instructor": {
                "bsonType": "string",
                "maxLength": 50,
                "description": "Name of the person teaching the section."
            }
        }
    }
}


def section_uniqueness(db):
    try:
        db.create_collection("sections")
    except Exception as error_message:
        pass
    db.command("collMod", "sections", validator=section_validation)
    collection = db["sections"]

    collection.create_index([("course_number", pymongo.ASCENDING), ("section_number", pymongo.ASCENDING),
                             ("semester", pymongo.ASCENDING), ("section_year", pymongo.ASCENDING)], unique=True)

    collection.create_index([("semester", pymongo.ASCENDING), ("section_year", pymongo.ASCENDING),
                             ("building", pymongo.ASCENDING), ("room", pymongo.ASCENDING),
                             ("schedule", pymongo.ASCENDING), ("start_time", pymongo.ASCENDING)], unique=True)

    collection.create_index([("semester", pymongo.ASCENDING), ("section_year", pymongo.ASCENDING),
                             ("schedule", pymongo.ASCENDING), ("start_time", pymongo.ASCENDING),
                             ("instructor", pymongo.ASCENDING)], unique=True)


def add_section(db):
    collection = db["sections"]
    success: bool = False

    while True:
        if success:
            break

        try:
            course = select_course(db)
            section_number = int(input("Section number--> "))
            semester = input("Semester section is offered--> ")
            section_year = int(input("Year section is offered--> "))
            building = input("Name of building of specific section--> ")
            room = int(input("Room number section is held in--> "))
            schedule = input("Day that section is offered--> ")
            start_time = input("Time that section starts--> ")
            instructor = input("Name of instructor teaching the section--> ")

            section = {
                "department_abbreviation": course.get("department_abbreviation"),
                "course_number": course.get("course_number"),
                "section_number": section_number,
                "semester": semester,
                "section_year": section_year,
                "building": building,
                "room": room,
                "schedule": schedule,
                "start_time": start_time,
                "instructor": instructor

            }
            new_section = collection.insert_one(section)

            filter_criteria = {"department_abbreviation": course.get("department_abbreviation"),
                               "course_number": course.get("course_number")}
            update = {"$push": {"sections": section}}
            result = db["courses"].update_one(filter_criteria, update)

            success = True
        except Exception as error_message:
            print("The following error occurred:", error_message)
            print("Make sure the information is valid")


def list_section(db):
    sections = db["sections"].find({}).sort([("section_number", pymongo.ASCENDING)])
    for section in sections:
        pprint(section)


def select_section(db):
    collection = db["sections"]
    found: bool = False
    department_abbreviation: str = ''
    course_number: int = -3
    section_semester: str = ''
    section_number: int = -1
    section_year: int = -2

    while not found:
        department_abbreviation = input("Enter the department abbreviation that the section is assigned to--> ")
        course_number = int(input("Enter the course number that the section is assigned to--> "))
        section_number = int(input("Enter the section number--> "))
        section_year = int(input("Enter the year section is offered--> "))
        section_semester = input("Enter the semester section is offered--> ")
        section_number_count: int = collection.count_documents({"department_abbreviation": department_abbreviation,
                                                                "course_number": course_number,
                                                                "section_number": section_number,
                                                                "section_year": section_year,
                                                                "semester": section_semester})
        found = section_number_count == 1
        if not found:
            print("No section was found.  Try again.")
    return_section = collection.find_one({"department_abbreviation": department_abbreviation,
                                          "course_number": course_number,
                                          "section_number": section_number, "section_year": section_year,
                                          "semester": section_semester})
    return return_section


def delete_section(db):
    section = select_section(db)
    sections = db["sections"]
    courses = db["courses"]

    update = courses.update_one({"department_abbreviation": section.get("department_abbreviation"),
                                 "course_number": section.get("course_number")},
                                {"$pull": {"sections": section}})

    deleted = sections.delete_one({"_id": section["_id"]})
    print(f"We just deleted: {deleted.deleted_count} section.")
