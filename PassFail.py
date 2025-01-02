import pymongo
from pymongo import MongoClient
from pprint import pprint
from datetime import datetime
from Enrollment import *


def PassFail_uniqueness(db):
    try:
        db.create_collection("pass_fails")
    except Exception as error_message:
        pass


def add_student_PassFail(db):
    collection = db["pass_fails"]
    success: bool = False

    while True:
        if success:
            break

        try:
            enrollment = select_enrollment(db)

            pass_fail = {
                "student_id": enrollment.get("student_id"),
                "application_date": datetime.now()
            }
            new_PassFail = collection.insert_one(pass_fail)

            filter_criteria = {"student_id": enrollment.get("student_id")}
            update = {"$set": {"pass_fail": datetime.now()}}
            result = db["enrollments"].update_one(filter_criteria, update)

            success = True
        except Exception as error_message:
            print("The following error occurred:", error_message)
            print("Make sure the information is valid")



