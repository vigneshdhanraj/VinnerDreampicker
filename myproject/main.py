import os
os.system("python manage.py migrate")
os.system("python manage.py makemigrations TeamPicker")
os.system("python manage.py migrate")
os.system("python manage.py runserver")
