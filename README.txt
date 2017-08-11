1- please install python 3 on your system (if not already installed). 


2- Open crawler folder, Install these  modules by typing in terminal/cmd:

$ pip install -r requirements
$ pip install beautifulsoup4

(OR individually install if above cause any problem !) 

$ pip install django
$ pip install beautifulsoup4
$ pip install django-crispy-forms
$ pip install Jinja2
$ python manage.py migrate

3- ONCE installed all requirements: 
now every time you want to run this application , open terminal/CMD in crawler folder. and type:    

$ python manage.py runserver

 And visit:
 "http://127.0.0.1:8000/" in your browser !