# Django Web Crawler


## Initial Form ##
```
```
* Website URL
* Check Broken Links
* Check Google Analytics Tracking Code
* Recaptcha
* startCrawling(Button)

## Features ##
```
* Limit of concurrent crawler jobs
* Progress indicator
* Generate summary at the end
* Export detailed summary & table to CSV/XML



## Requirements Installation ##
```
1- Python3
2- Open terminal/cmd in code folder & run:
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
