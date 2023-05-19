![Classroom Sync](images/classroom-sync.png)
# Classroom Sync Suite
These are a collection of tools for working with GitHub Classroom assignments.  

## Classroom Sync
This tool pulls a list of students from a Canvas course, then uses the provided roster.csv file to map the the Canvas user names to github user names. It then retrieves student repositories for the specified assignment and renames them to include Canvas username instead of their GitHub username.

```
Usage: classroom-sync.py <assignment> 
    assignment - You can find the list of assignment names on GitHub Classroom
```

## Classroom Sync Basic
The original version of this tool did not have a dependency upon Canvas and instead the flow is simply for each entry in the roster.csv file, retrieve the student repository for the specified assignment and rename it to use the institution username from the mapping.  

```
Usage: classroom-sync-basic.py <assignment> 
    assignment - You can find the list of assignment names on GitHub Classroom
```

## Before using this tool, do the following:
1. Set up SSH key-based authentication with GitHub  
2. Download the classroom_roster.csv file from GitHub Classroom  
3. Update classroom-config.json with the details for your classroom  
4. Enable API access for Canvas user account and store token in OS keyring. Details are provided below

## Installation Notes
This tool requires python3.8 and the pip utility as well as the following python modules:
```
pip install canvasapi
pip install keyring
```

## Canvas API Notes
Instead of embedding the canvas token, I am using the python keyring library to integrate with the operating systems keystore.  Once the python modules are installed, use the following command-line options to add the required values to the OS level keystore. To create an Access Token in Canvas do the following:

Go to Account, Settings, New Access Token with reason “To Synchronize Github Classrooms and Grades"

```
keyring set canvas url
# set password to the following:  https://boisestatecanvas.instructure.com/
keyring set canvas token
# set password to the following:  <dev token from Canvas>
```

## Development Notes
This code was developed and tested on Ubuntu 20.04 running Python 3.8.10



