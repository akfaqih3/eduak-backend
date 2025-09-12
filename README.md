# eduak-backend

### DESCRIPTION

This is the backend for eduak platform.

### FEATURES

- Authentication by email and password.
- Authorization by JWT(Json Web Token).
- Custom user model for teachers and students.
- Users operations (registration, login, logout, profile, forgot password, password change, email verification).
- CRUD operations for teachers and courses.
- API documentation by swagger ui.

### PROJECT STRUCTURE

```
eduak-backend/
├── config/
│   ├── __init__.py
│   ├── settings.py
│   │   ├── base.py # base settings for the project
│   │   ├── development.py # development settings for the project
│   │   ├── production.py # production settings for the project
│   ├── urls.py
│   └── wsgi.py
├── accounts/
│   ├── __init__.py
│   ├── admin.py
│   ├── authentications.py # custom authentication backend
│   ├── models.py 
│   ├── serializers.py 
│   ├── services.py # create and update functions for this app
│   ├── signals.py # signals ( groups creation, password reset token, etc.)
│   ├── urls.py
│   ├── utils.py # utility classes (limit login attempts, otp manager, etc.)
│   ├── validators.py # validators (email,phone, password, etc.)
│   └── views.py
├── teachers/
│   ├── __init__.py
│   ├── admin.py
│   ├── models.py
│   ├── permissions.py # custom permissions for teachers
│   ├── selectors.py # get data from database
│   ├── serializers.py
│   ├── services.py # cud operations for courses 
│   ├── urls.py
│   └── views.py # api views for teachers
├── courses/
│   ├── __init__.py
│   ├── admin.py
│   ├── models.py
│   ├── permissions.py # custom permissions for courses
│   ├── selectors.py # get data from database
│   ├── serializers.py
│   ├── services.py # cud operations for courses 
│   ├── urls.py
│   └── views.py # api views for courses
├── manage.py
```



### INSTALLATION
## get project from github

```bash
git clone https://github.com/akfaqih3/lomfu-backend.git
```

## change directory to project

```bash
cd eduak-backend
```

## create virtual environment

```bash
python -m venv .venv
```

## activate virtual environment

```bash
source .venv/bin/activate #linux or mac
.venv\Scripts\activate #windows
```

## install dependencies

```bash
pip install -r requirements.txt
```

## create .env file for environment variable

paste this in .env file you have created:

```
# app settings
APP_NAME= #your app name here
SECRET_KEY= # your project secret key here

# database settings
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# email settings
EMAIL_HOST_USER = akram@example.com
EMAIL_HOST_PASSWORD = # paste app password here
DEFAULT_FROM_EMAIL = akram@example.com

# GOOGLE SETTINGS
GOOGLE_CLIENT_ID = # paste your google client id here
GOOGLE_CLIENT_SECRET = # paste your google client secret here
GOOGLE_REDIRECT_URI = http://127.0.0.1:8000/api/v1/accounts/google/login/

```

## migrate database

```bash
python manage.py migrate
```

# create super user

```bash
python manage.py createsuperuser
    # email: admin@example.com
    # password: admin
    # password (again): admin
```

## Run 

```bash
python manage.py runserver
    # http://127.0.0.1:8000/swagger/
```


## github repo  go to https://github.com/akfaqih3/eduak-backend



