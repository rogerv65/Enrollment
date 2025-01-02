import pymongo
from pymongo import MongoClient
from pprint import pprint

department_validation = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["name", "abbreviation", "chair_name", "building", "office", "description"],
        "properties": {
            "name": {
                "bsonType": "string",
                "minLength": 10,
                "maxLength": 50,
                "description": "What the department is called."
            },
            "abbreviation": {
                "bsonType": "string",
                "maxLength": 6,
                "description": "An acronym for the specified department."
            },
            "chair_name": {
                "bsonType": "string",
                "maxLength": 80,
                "description": "Name of the person in charge of the department."
            },
            "building": {
                "enum": ['ANAC', 'CDC', 'DC', 'ECS', 'EN2', 'EN3', 'EN4', 'EN5', 'ET', 'HSCI', 'NUR', 'VEC'],
                "description": "The structure that the department is located in."
            },
            "office": {
                "bsonType": "number",
                "description": "The room number that department's chair is located in."
            },
            "description": {
                "bsonType": "string",
                "maxLength": 80,
                "description": "A text that explains the department."
            }
        }
    }
}


def department_uniqueness(db):
    # Checks if department database exists
    # If it doesn't, creates a new department, if it does, reuses the old department
    try:
        db.create_collection("departments")
    except Exception as error_message:
        pass
    # Ensuring each property of the department class is unique
    db.command("collMod", "departments", validator=department_validation)
    collection = db["departments"]
    collection.create_index([("name", pymongo.ASCENDING)], unique=True)
    collection.create_index([("abbreviation", pymongo.ASCENDING)], unique=True)
    collection.create_index([("chair_name", pymongo.ASCENDING)], unique=True)
    collection.create_index([("building", pymongo.ASCENDING), ("office", pymongo.ASCENDING)], unique=True)


def add_department(db):
    collection = db["departments"]
    success: bool = False

    while True:
        if success:
            break

        try:
            name = input("Department name--> ")
            abbreviation = input("Department abbreviation--> ")
            chair_name = input("Chair name--> ")
            building = input("Building --> ")
            office = int(input("Office number --> "))
            description = input("Description of department --> ")

            department = {
                "name": name,
                "abbreviation": abbreviation,
                "chair_name": chair_name,
                "building": building,
                "office": office,
                "description": description,
                "courses": [],
                "majors": []
            }

            new_department = collection.insert_one(department)
            success = True
        except Exception as error_message:
            print("The following error occurred:", error_message)
            print("Make sure the information is valid")


def list_department(db):
    departments = db["departments"].find({}).sort([("name", pymongo.ASCENDING)])
    for department in departments:
        pprint(department)


def select_department(db):
    collection = db["departments"]
    found: bool = False
    abbreviation: str = ''

    while not found:
        abbreviation = input("Enter the department abbreviation--> ")
        abbreviation_count: int = collection.count_documents({"abbreviation": abbreviation})
        found = abbreviation_count == 1
        if not found:
            print("No department with that abbreviation.  Try again.")
    return_department = collection.find_one({"abbreviation": abbreviation})
    return return_department


def delete_department(db):
    department = select_department(db)
    departments = db["departments"]

    if department and "courses" in department:
        if len(department["courses"]) != 0:
            print("Can't delete this department because a course is connected to it.")

        else:
            if department and "majors" in department:
                if len(department["majors"]) != 0:
                    print("Can't delete this department because a major is connected to it.")

                else:
                    deleted = departments.delete_one({"_id": department["_id"]})
                    print(f"We just deleted: {deleted.deleted_count} department.")
