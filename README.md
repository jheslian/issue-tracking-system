
# An issue tracker API for differents platforms (website, Android and iOS apps).

## Objectives:
- The API basically allow users to create various projects, add users to specific projects, create issues within the projects, and assign labels to those issues based on their priorities, tags, and more.
- The application is created with django rest framework with simpleJWT as a default authentication



## Features of the application:
|Functionnalities  | Remarks |
|---|---|
| User authentication (registration/login) | *Used JWT authentication to authenticate users.* |
| Users must have access to basic **_CRUD-type_** actions (Create, Read, Update, and. Delete) on projects | *A project can be defined as an entity with multiple collaborators (users), and each project can contain multiple issues.*
|  _Each project can have issues associated with it; the user should only be able to apply the_ **_CRUD process to_** _project issues_ **_if_** _he or she is on the list of contributors._| _A project should only be accessible to its manager and contributors. Only contributors are allowed to create or view issues in a project._ |
| _Each issue hasa_ **_title_** _,_ **_description_** _,_ **_assignee_** _(default assignee being the author himself),_ **_priority_** _(LOW, MEDIUM, or HIGH),_ **_tag_** _(BUG, IMPROVEMENT, or TASK),_ **_status_** _( To Do, In Progress, or Done), the_ **_project_id_** _it's linked to, and a_ **_created_time_** _(timestamp), and other attributes._ |_Only contributors can create (Create) and read (Read) comments related to an issue. In addition, they can only update (Update) and delete (Delete) them if they are the authors._  |
| _Issues can be commented on by contributors to the project to which those issues belong. Each comment must have a_ **_description_** _,_ **_author_user_id_** _,_ **_issue_id ,_** _and_ **_comment_id_** _._ | _A comment must be visible to all project contributors, but can only be updated or deleted by its author._ |
| _Any authorized user other than the author is_ **_prohibited_** _to update and delete an_ **_issue/project/comment_** _._|*Author can only perform update and delete*|


## API Documentation:
Check the documention how to use the API and see some examples : [Issue Tacking API](https://documenter.getpostman.com/view/19593881/UyxdJoJT)


## Application environments:
 - python: version 3.8
 - django: 4.0
 - *complete packages used are in requirements.txt*


## Getting started:
**Note**: Make sure you have python(atleast version 3.8) , virtual environment and git on your machine:
	- `python -V` : command to check the version python if its installed
	- verify that you have the venv module : `python -m venv --help` if not please check https://www.python.org/downloads/. You could also use any other virtual environment to run the program(**if you opted to use other virtual environment the next commands are not suitable to run the program**)
	- `git --version` : to check your git version if its installed or you could download it at https://git-scm.com/downloads
 1. Clone the repository on the terminal or command prompt : `git clone https://github.com/jheslian/issue-tracking-system.git`
 2. Create a virtual environment with "venv"  
	 - `cd issue-tracking-system` :  to access the folder 
	 - python -m venv ***environment name*** : to create the virtual environment - exemple: `python -m venv env`
3. Activate the virtual environment:
	for unix or macos:
	- source ***environment name***/bin/activate - ex : `source env/bin/activate` if "env" is used as environment name 
	for windows:
	- ***environment name***\Scripts\activate.bat - ex: `env\Scripts\activate.bat`
4. Install the packages with pip: `pip install -r requirements.txt`	
5.  Migrate the tables to database:
    for unix or macos: `python3 manage.py migrate`
	for windows: `py manage.py migrate`
6. Run the program :
	for unix or macos: `python3 manage.py runserver`
	for windows: `py manage.py runserver`
	***Note*** : The default port will open at 8000.
