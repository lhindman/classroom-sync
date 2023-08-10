![Classroom Sync](images/classroom-sync.png)
# Classroom Sync Suite
These are a collection of tools for working with GitHub Classroom assignments.  

### SSH Agent
Before running the tools below, please be certain to start the SSH Agent and add your local ssh key. The sync tools make a unique connection to github for each and if there is a password on the key, it will prompt for the password on each connection.  The SSH-Agent will cache the unlocked key for the duration of the shell session.

```
   ssh-agent
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

## Before using this tool, do the following:
1. Set up SSH key-based authentication with GitHub  
2. Download the classroom_roster.csv file from GitHub Classroom  
3. Update classroom-config.json with the details for your classroom  
4. Enable API access for Canvas user account and store token in OS keyring. Details are provided below

## Installation Notes
This tool requires python3.8 and the pip utility as well as the following python modules:
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
CANVAS_TOKEN=<paste token here>
```
The .gitignore file include **.env** to prevent this file from accidentally being pushed to github.

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



