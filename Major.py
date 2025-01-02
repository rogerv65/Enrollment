import pymongo
from pymongo import MongoClient
from pprint import pprint
from Department import *

major_validation = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["name", "description"],
        "properties": {
            "name": {
                "bsonType": "string",
                "maxLength": 50,
                "description": "What the major is called."
            },
            "description": {
                "bsonType": "string",
                "maxLength": 80,
                "description": "The description of the major."
            }

        }
    }
}


def major_uniqueness(db):
    try:
        db.create_collection("majors")
    except Exception as error_message:
        pass
    db.command("collMod", "majors", validator=major_validation)
    collection = db["majors"]
    collection.create_index([("name", pymongo.ASCENDING)], unique=True)


def add_major(db):
    collection = db["majors"]
    success: bool = False

    while True:
        if success:
            break

        try:
            department = select_department(db)
            name = input("Name of major --> ")
            description = input("Description of major --> ")
            majors = {
                "department_abbreviation": department.get("abbreviation"),
                "name": name,
                "description": description,
            }
            new_major = collection.insert_one(majors)

            filter_criteria = {"abbreviation": department.get("abbreviation")}
            update = {"$push": {"majors": majors}}
            result = db["departments"].update_one(filter_criteria, update)

            success = True
        except Exception as error_message:
            print("The following error occurred:", error_message)
            print("Make sure the information is valid")


def list_major(db):
    majors = db["majors"].find({}).sort([("name", pymongo.ASCENDING)])
    for major in majors:
        pprint(major)


def select_major(db):
    collection = db["majors"]
    found: bool = False
    major_name: str = ''

    while not found:
        major_name = input("Enter the name of the major--> ")
        major_name_count: int = collection.count_documents({"name": major_name})
        found = major_name_count == 1
        if not found:
            print("No major with that name.  Try again.")
    return_major = collection.find_one({"name": major_name})
    return return_major


def delete_major(db):
    major = select_major(db)
    majors = db["majors"]
    departments = db["departments"]
    student_major = db["student_majors"]

    update = departments.update_one({"abbreviation": major.get("department_abbreviation")},
                                    {"$pull": {"majors": major}})

    deleted = majors.delete_one({"_id": major["_id"]})
    print(f"We just deleted: {deleted.deleted_count} major.")
