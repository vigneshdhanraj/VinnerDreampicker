# VinnerDreampicker
## Dream Team Picker 

Create Virtual Environment and Install packages needed
```bash
virtualenv myenv --python=python3
source myenv/bin/activate
pip install django
```

## Run the Following commands to get Started Default DB created needed migrate if added anything in Models
```bash
cd myproject/
python manage.py migrate
python manage.py makemigrations TeamPicker
python manage.py migrate
```

## Run the Django WebServer Using Following Command
```bash
python manage.py runserver
```
Once Server started Access the DreamPicker using 

```
http://127.0.0.1:8000/
```

## Project is Implementated Using Django Framework
