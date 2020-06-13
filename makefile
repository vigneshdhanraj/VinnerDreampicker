# Resume Parser Make File
  
VIRTUALENV = $(shell which virtualenv)

run:
	. myenv/bin/activate; python myproject/manage.py runserver

