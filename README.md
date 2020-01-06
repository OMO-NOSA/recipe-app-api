### Description

This repository contains the backend code of the recipe application and its APIs.

### Dependencies
* python3.7

### Install Python 
install from official python site
[Python](https://www.python.org/downloads/)

### Post clone commands
```sh
cd project directory
```
### Run commands
```sh
pip install virtualenv
```
### Activate Virtualenv
```sh
source env/Scripts/activate
```
### Install project Dependencies from pipfile.lock
```sh
pip install -r requirements.txt 
```

### Change Directory into Project Dir with Manage.py file
```sh
cd VMS
```

### Run Django Development Server
```sh
python manage.py runserver
```

### Using Docker
* Make sure your are in the root directory that contains the DockerFile

### Run commands to build DockerFile
```sh
docker build -t app .
```
### Run commands to Run DockerFile
```sh
docker run --name app -p 8000:8000 -d django-app
```

### Test on the Browser:
* visit http://container-ip:8000 in a browser or, if you need access outside the host,  on http://localhost:8000