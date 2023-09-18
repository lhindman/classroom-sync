#!/usr/bin/env python3
# Author:  Luke Hindman
# Date: Wed 17 May 2023 01:55:54 PM MDT
# Description: Sync tool for GitHub Classroom assignments
#     This tool will retrieve student repositories and rename them
#        to include Canvas username instead of their
#        GitHub username.
#
#     Before using this tool, do the following:
#       1. Set up SSH keybased authentication with GitHub  
#       2. Download the classroom_roster.csv file from GitHub Classroom  
#       3. Update classroom-config.json with the details for your classroom  
#       4. Enable API access for Canvas user account and store token in OS keyring. Details are provided below
#
#  Usage: classroom-sync.py <assignment> 
#
#   assignment - You can find the list of assignment names on GitHub Classroom



import csv
import sys
import os
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


# Return a dictionay containing the github roster mapping
#   with the key valuing being the Canvas username
#   and the value being the github username.
def get_github_roster(roster_file):
    github_roster = {}

    if roster_file == "":
        return github_roster

    roster_list = []
    with open(roster_file,'r',encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, dialect='excel')
        for line in reader:
            roster_list.append(line)

    for entry in roster_list:
        canvas_username = entry['identifier'].split('@')[0].lower()
        github_roster[canvas_username] = entry['github_username']

    return github_roster


def clone_student_repos(students,github_roster,github_organization,assignment_name,classroom_path,student_filter):

    # GitHub repo URLs are in lowercase, so convert specified
    #    assignment name for consistency
    assignment_name = assignment_name.lower()

    # Setup classroom and assignment directory structure 
    if not os.path.isdir(classroom_path):
        os.mkdir(classroom_path)

    assignment_path = os.path.join(classroom_path,assignment_name) 
    if not os.path.isdir(assignment_path):
        os.mkdir(assignment_path)

    repo_status = {}
    num_students = len(students)
    student_count = 1
    print("Cloning Student Repos\n\n")
    for student in students.values():
        canvas_username = student.login_id
        if canvas_username.lower() not in github_roster.keys():
            print("- Warning: User not found on GitHub roster: " + canvas_username)
            repo_status[canvas_username] = "User not found on GitHub roster"
            continue
        github_username = github_roster[canvas_username.lower()]

        if student_filter is None or (student_filter is not None and canvas_username.lower() == student_filter):
            print("%-40s (%s)" % (canvas_username, str(student_count) + "/" + str(num_students)))
            student_count = student_count + 1

            # Skip users with no mapping to GitHub accounts
            if github_username == "":
                print("- Warning: No GitHub mapping exists for user: " + canvas_username)
                repo_status[canvas_username] = "No GitHub mapping exists"
                continue

            url="git@github.com:" + github_organization + "/" + assignment_name + "-" + github_username + ".git"
            try: 
                entry_path = os.path.join(assignment_path,canvas_username)
                if os.path.isdir(os.path.join(entry_path,".git")):
                    subprocess.run(['git','pull'],cwd=entry_path,capture_output=True,timeout=20,check=True,text=True)
                    repo_status[canvas_username] = "Repo pulled successfully: %s" % (url)
                else:
                    subprocess.run(['git','clone', url, canvas_username],cwd=assignment_path,capture_output=True,timeout=20,check=True,text=True)
                    repo_status[canvas_username] = "Repo cloned successfully: %s" % (url)
            except CalledProcessError as e:
                print("- Warning: Unable to clone repo: " + url)
                repo_status[canvas_username] = "Error while cloning repository"
            except subprocess.TimeoutExpired as e:
                print("- Warning: Unable to clone repo (timeout): " + url)
                repo_status[canvas_username] = "Timeout while cloning repository"

    return repo_status


def main():
    
    # Check the parameters
    if len(sys.argv) < 2:
        print("usage: classroom-sync.py <assignment>")
        sys.exit(1)

    # Parse the command line args
    assignment = sys.argv[1]

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

    # Load GitHub Roster and store to dictionary, indexed by Canvas username in lowercase
    github_roster = get_github_roster(roster_file)

    clone_student_repos(canvas_students,github_roster,github_org,assignment,classroom_path,student_filter=None)


if __name__ == '__main__':
	main()
