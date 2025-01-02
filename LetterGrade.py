import pymongo
from pymongo import MongoClient
from pprint import pprint
from Enrollment import *


def LetterGrade_uniqueness(db):
    try:
        db.create_collection("letter_grades")
    except Exception as error_message:
        pass


def add_student_LetterGrade(db):
    collection = db["letter_grades"]
    success: bool = False

    while True:
        if success:
            break

        try:
            enrollment = select_enrollment(db)

            minSatisfactory = input("Select the minimum letter grade ('A', 'B', 'C'): ")
            while minSatisfactory != 'A' and minSatisfactory != 'B' and minSatisfactory != 'C':
                minSatisfactory = input("The minimum grade must be a valid grade ('A', 'B', 'C'): ")

            letter_grade = {
                "student_id": enrollment.get("student_id"),
                "min_satisfactory": minSatisfactory
            }
            new_LetterGrade = collection.insert_one(letter_grade)

            filter_criteria = {"student_id": enrollment.get("student_id")}
            update = {"$set": {"letter_grade": minSatisfactory}}
            result = db["enrollments"].update_one(filter_criteria, update)

            success = True
        except Exception as error_message:
            print("The following error occurred:", error_message)
            print("Make sure the information is valid")
