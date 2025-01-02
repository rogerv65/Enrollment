import pymongo
from pymongo import MongoClient
from pprint import pprint
import getpass
import certifi
from Department import *
from Course import *
from Section import *
from Major import *
from Student import *
from Enrollment import *
from Student_Major import *
from LetterGrade import *
from PassFail import *
from menu_definitions import menu_main
from menu_definitions import add_menu
from menu_definitions import delete_menu
from menu_definitions import list_menu


def add(db):
    """
    Present the add menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    add_action: str = ''
    while add_action != add_menu.last_action():
        add_action = add_menu.menu_prompt()
        exec(add_action)


def delete(db):
    """
    Present the delete menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    delete_action: str = ''
    while delete_action != delete_menu.last_action():
        delete_action = delete_menu.menu_prompt()
        exec(delete_action)


def list_objects(db):
    """
    Present the list menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    list_action: str = ''
    while list_action != list_menu.last_action():
        list_action = list_menu.menu_prompt()
        exec(list_action)

if __name__ == '__main__':
    cluster = "Insert your mongodb cluser here!"
    client = MongoClient(cluster, tlsCAFile=certifi.where())
    # As a test that the connection worked, print out the database names.
    # print(client.list_database_names())
    # db will be the way that we refer to the database from here on out.
    db = client["Demonstration"]
    # Print off the collections that we have available to us, again more of a test than anything.
    # print(db.list_collection_names())
    # student is our students collection within this database.
    # Merely referencing this collection will create it, although it won't show up in Atlas until
    # we insert our first document into this collection.

    main_action: str = ''
    department_uniqueness(db)
    course_uniqueness(db)
    section_uniqueness(db)
    major_uniqueness(db)
    student_uniqueness(db)
    enrollment_uniqueness(db)
    student_major_uniqueness(db)
    LetterGrade_uniqueness(db)
    PassFail_uniqueness(db)

    while main_action != menu_main.last_action():
        main_action = menu_main.menu_prompt()
        print('next action: ', main_action)
        exec(main_action)
