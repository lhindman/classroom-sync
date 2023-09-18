
import keyring
from canvasapi import Canvas
import decouple
from decouple import config

# Loads the canvas URL and security token from the system keystore.
# These can be set using the keyring command as follows:
#    keyring set canvas token
def canvas_connect(api_url):
    # Canvas API key from .env file or CANVAS_TOKEN environment
    #    variable. If this fails, fall back to the OS keyring.
    try: 
        API_KEY = config('CANVAS_TOKEN') 
    except decouple.UndefinedValueError:
        API_KEY = keyring.get_password("canvas","token")

    # Initialize a new Canvas object
    canvas = Canvas(api_url, API_KEY)

    return canvas

# Iterates through the list of active courses and returns
#   a course object that matches the specified course_name
#   and course code. if no matching course is found, returns None
def canvas_get_course(canvas,course_code,course_name):
    course_dict={}
    course_match = None
    for course in canvas.get_courses(state=['available']):
        
        # Courses that are published, but that are date restricted are still considered "available" :(
        #   This causes access errors and therefore need to be excluded.
        if "access_restricted_by_date" in course.__dict__.keys():
            continue

        if course_code == course.course_code and course_name == course.name:
            course_match = course

    return course_match


# Return a dictionary containing User objects of students
#   enrolled the specified course. The dictionary keys
#   are the canvas user_id numbers.
def canvas_get_students(course):
    student_dict={}
    for user in course.get_users(enrollment_type=['student']):
        student_dict[user.id] = user
    
    return student_dict