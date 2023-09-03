![Classroom Sync](images/classroom-sync.png)
# Classroom Sync Suite
These are a collection of tools for working with GitHub Classroom assignments.  

### SSH Agent
Before running the tools below, please be certain to start the SSH Agent and add your local ssh key. The sync tools make a unique connection to github for each student repository and if there is a password on the key, it will prompt for the password on each connection.  The SSH-Agent will cache the unlocked key for the duration of the shell session.

To ensure that the environment variables are configured correctly when starting the ssh-agent, it must be executed using the eval command. This may not be necessary on MacOS systems.

```
   eval $(ssh-agent)
   ssh-add
```

### Classroom Sync (Canvas)
This tool pulls a list of students from a Canvas course, then uses the provided roster.csv file to map the the Canvas user names to github user names. It then retrieves student repositories for the specified assignment and renames them to include Canvas username instead of their GitHub username.

```
Usage: classroom-sync.py <assignment> 
    assignment - You can find the list of assignment names on GitHub Classroom
```

### Classroom Sync (Basic)
The original version of this tool did not have a dependency upon Canvas and instead the flow is simply for each entry in the roster.csv file, retrieve the student repository for the specified assignment and rename it to use the institution username from the mapping.  

```
Usage: classroom-sync-basic.py <assignment> 
    assignment - You can find the list of assignment names on GitHub Classroom
```

### Commit and Push Grades (Canvas)
This tool will commit and push GRADE.md files, located within student repositories, to GitHub.  It first connects to Canvas to retrieve the student roster. For each student it then opens the local repo in the specified assignment folder and stages (adds) each GRADE.md to a single commit which is then pushed to GitHub. Since it is possible for a single repositories to contain multiple coding projects, multiple GRADE.md files may be found and pushed to GitHub for a single repository.

While not strictly necessay, by using the Canvas roster this tool can display info regarding students who not not have a local repository or who do not have a GitHub mapping. This can be helpful for debugging purposes or for razing the visibility of students who are not completing the assignments.

NOTE:  This tool is designed to be used on student repositories that have previousoly been cloned from GitHub using the classroom-sync.py tool described above.

```
Usage: commit-and-push-grades.py <assignment> 
    assignment - You can find the list of assignment names on GitHub Classroom
```

### Calculate Totals and Summarize (Canvas)
This tool will parse the GRADE.md file located in each student repository, sum the scores from each rubric section and insert a row containing the total value. Once complete, it will generate a CSV file containing a summary of student scores for the specified assignment.

```
The following shows the sections that will be processed:  
Planning                        /6  
Subject Proficiency             /12  
Coding Conventions              /3  
Terminology Identification      /3  
Code Review                     /2  
Reflection                      /4  
-----------------------------------  
Total                         30/30  (inserted by script)
```

The line containing the Total is inserted into the GRADE.md in each student repository for the specified assignment.  Once completed, a CSV file is generated in the current directory that contains a summary of all the student scores for the specified assignments.
```
Usage: calculate_totals_and_summaryize.py <assignment> 
   assignment - You can find the list of assignment names on GitHub Classroom
```

## Before using these tool, do the following:
1. Clone this repository into your local development environment
2. Set up SSH key-based authentication with GitHub  
3. Download the classroom-roster.csv file from GitHub Classroom  
4. Update classroom-config.json with the details for your classroom  
5. Enable API access for Canvas user account and store token in OS keyring. Details are provided below

## Installation Notes
This tool requires a minimum of python version 3.8 and the corresponding pip utility. You can confirm you are running the correct versions using the following commands:
```
Last login: Sun Sep  3 10:30:02 on ttys001
(base) platypus@sa-angreal classroom-sync % which python3
/Users/platypus/anaconda3/bin/python3
(base) platypus@sa-angreal classroom-sync % which pip3
/Users/platypus/anaconda3/bin/pip3
(base) platypus@sa-angreal classroom-sync % python3 --version
Python 3.11.4
(base) platypus@sa-angreal classroom-sync % 
```

Once the minimum Python version has been confirmed and that the version of pip3 is in the same folder as the active version of python, please install the following modules:
```
pip3 install canvasapi
pip3 install keyring
pip3 install python-decouple
```

## Canvas API Notes
Instead of embedding the canvas token, I am using the python keyring library to integrate with the operating systems keystore.  Once the python modules are installed, use the following command-line options to add the required values to the OS level keystore.  

#### Generate Canvas Token
To create an Access Token in Canvas do the following:
- Go to Account, Settings, New Access Token with reason “To Synchronize Github Classrooms and Grades"

#### Store Canvas Token in OS Keyring
This is the preferred method for storing the Canvas token because it is encrypted within the Operating System's keystore
```
keyring set canvas token
# set password to the following:  <dev token from Canvas>
```
#### Store Canvas Token in file
Linux systems running the Gnome Keyring Manager, such as RedHat Enterprise Linux, do not support unlocking the keyring from the command line or over an ssh session. To work around this issue, the Canvas token can be stored in a text file called **.env** in the same directory as the sync scripts, and then read as an environment variable within the sync scripts.
```
touch .env
chmod 0600 .env
vim .env
CANVAS_TOKEN=<dev token from Canvas>
```
The *.gitignore* file excludes **.env** to prevent this file from accidentally being pushed to github.

## Running on remote Linux system over SSH
If the system has multiple versions of Python installed, it is helpful to specify the explicit version of python (and pip) to use. Depending upon the security settings, pip may require the **--user** flag in order to install the modules into the users home directory.
```
pip3.8 install --user canvasapi
pip3.8 install --user keyring
pip3.8 install --user python-decouple
```

When running the sync scripts, it will use the default python3 interpreter. However, with multiple versions of python installed, it is helpful to specify this explictly as well.

```
python3.8 classroom-sync.py <assignment>
python3.8 classroom-sync-basic.py <assignment>
python3.8 commit-and-push-grades.py <assignment>
```

## Development Notes
This code was developed and tested on Ubuntu 20.04 running Python 3.8.10
Additional testing has been performed on MacOS 12.4 and RHEL 8.



