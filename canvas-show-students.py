#!/usr/bin/env python3
# Author:  Luke Hindman
# Date: Wed 17 May 2023 01:55:54 PM MDT
# Description: List the students and account names for the Canvas roster. This tool can be used
#     to verify that the connection to the Canvas classroom is functioning properly.
#
#     Before using this tool, do the following:
#       1. Update classroom-config.json with the details for your classroom  
#       2. Enable API access for Canvas user account and store token in OS keyring. Details are provided below
#
#  Usage: canvas-show-students.py 
#

import csv
import sys
import os
import os.path
import json
import subprocess
from subprocess import CalledProcessError

import canvastools

# Returns a dictionary containing the classroom
#    configuration information loaded from
#    the specified json formatted config_file.
def load_classroom_config(config_file):
    map_data = {}
    with open(config_file) as json_file:
        map_data = json.load(json_file)
    return map_data


def main():

    # Load the classroom configuration data
    classroom_config = load_classroom_config("classroom-config.json")
    roster_file = classroom_config['global']['github-roster']
    classroom_path = classroom_config['global']['classroom-path']
    course_name = classroom_config['global']['canvas-course-name']
    course_code = classroom_config['global']['canvas-course-code']
    api_url = classroom_config['global']['canvas-url']
    github_org = classroom_config['global']['github-org']


    # Connect to the Canvas gradebook
    canvas = canvastools.canvas_connect(api_url)

    if canvas == None:
        print("Error: Unable to connect to Canvas ")
        sys.exit(1)

    canvas_course = canvastools.canvas_get_course(canvas,course_code,course_name)

    if canvas_course == None:
        print("Error: Unable to Canvas course match: %s (%s) " % (course_name,course_code))
        sys.exit(1)

    canvas_students = canvastools.canvas_get_students(canvas_course)

    print("Course Name: %s" % canvas_course.name)
    email_list = []
    for student in canvas_students.values():
        print("%s (%s)" % (student.name,student.login_id))
        print("------------------")
        email_list.append(student.email)
    
    print("Student Emails:")

    print(",".join(email_list))



if __name__ == '__main__':
	main()
