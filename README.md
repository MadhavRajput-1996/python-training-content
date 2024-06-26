## This repo contain python training content and practical examples of varios python topics.

### Requirements:

1. Install anaconda. 
2. Python environment setup using conda commands. Also download jupyter notebook (python with latest version with some libraries will be installed i.e python 3.12.3)
3. Activate the virtual environment.
4. Enable jupyter extension in vscode.
5. Configure python environment in vscode to run jupiter files (ipynb files).
6. For text based content create markdown in jupyter.

### Training Levels 

1. Basic python concepy (level 1)

   code directory:- pt1-python-basic

   i.e variables, operators, control statements, datatypes.

2. Oops concept in python (level 2)
  
   code directory:- pt2-python-oops

   i.e functions, modules, packages, all oops based topics.

3. Advance python concept (level 3)

   code directory:- pt3-python-advance 

   i.e Iterators, Generators, Decorators, Closure, Regular Expressions, Exception Handling,   File Handling, Database Handling.

4. Python Frameworks (level 4)

   code directory:- pt4-python-frameworks-project

   i.e Django and Flask frameworks basics with some projects.

### Commands to run 

1. Migration commands:
   
   cd path/to/your/project
   python manage.py makemigrations
   python manage.py migrate
   
2. Faker data feed command: 

   cd path/to/your/project
   python manage.py populate_todos

### Steps to upload and run project on pythonanywhere

1. Create an account
2. Go to web tab and click on add a new web app
3. select django, select python version and give project a name.
4. Go to console tab and click on bash
5. git clone your project there
6. Do couple of more stuff inside web tab
   
   - scroll down and go to WSGI configuration file: "set your project home by copying the path using bash"
      - i.e /home/madhav1996/python-training-content/pt4-python-frameworks-project/django5_todo_project
   - also set environment variable to tell django where your settings.py is
      - i.e os.environ['DJANGO_SETTINGS_MODULE'] = 'django5_todo_project.settings'
   - Set Static files:
      - "give the static file path of your project"
     
8. Open your settings.py using nano in bash and do the following

   - import os
   - enter ALLOWED_HOSTS = ['madhav1996.pythonanywhere.com']
   - STATIC_URL = '/static/' and STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
   - Finally Run "python manage.py collectstatic" command
      
9. Go to your pythonanywhere web tab and reload the site
     - i.e https://www.pythonanywhere.com/user/madhav1996/webapps 
     


   
   



   
