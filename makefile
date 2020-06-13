# Resume Parser Make File
  
VIRTUALENV = $(shell which virtualenv)

clean:
	rm -rf myenv
	find . -name "*.pyc" -exec rm -f {} \;

install: clean
	virtualenv myenv --python=python3
	. myenv/bin/activate;pip install django
	. myenv/bin/activate;python myproject/manage.py migrate
	. myenv/bin/activate;python myproject/manage.py makemigrations TeamPicker
	. myenv/bin/activate;python myproject/manage.py migrate

run:
	. myenv/bin/activate; python myproject/manage.py runserver

