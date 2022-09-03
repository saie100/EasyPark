# Installing and running backend Django server

## Packages and dependencies installs
Installing pip3 (If you have pip3, skip this step)
```console
sudo apt install python3-pip
```
Installing postgresql database (If you have postgresql, skip this step)
```console
sudo apt install postgresql postgresql-contrib
```
Installing django and dependencies
```console
python3 -m pip install django==4.0.4
python3 -m pip install djangorestframework
python3 -m pip install django-cors-headers
python3 -m pip install django-secure-password-input
python3 -m pip install psycopg2-binary
```

## Django server
In the "easypark_backend" root directory, run the following commands:
```console
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```


