# eduak-backend

### DESCRIPTION


This is the backend for eduak project - A modern E-learning platform built with Django REST Framework.


### FEATURES

- 🔐 Authentication by email and password
- 🎫 Authorization by JWT (Json Web Token) with token rotation and blacklisting
- 👥 Custom user model for teachers and students
- 📧 Email verification with OTP
- 🔑 Google OAuth2 authentication
- 👨‍🏫 CRUD operations for teachers and courses
- 📚 Course management with modules and content
- 🎓 Student enrollment system
- 📖 API documentation by Swagger UI and ReDoc
- 🚀 Rate limiting for API protection
- 🔒 Security best practices implemented
- 🐳 Docker support for easy deployment
- 📊 Database indexing for better performance

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
git clone https://github.com/akfaqih3/eduak-backend.git
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


## Docker Deployment (Recommended)

### Using Docker Compose

```bash
# Build and run containers
docker-compose up -d --build

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Access the application
# http://localhost:8000/swagger/
```

## Production Deployment

### Additional Settings for Production

Add these to your .env file:

```
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### Security Checklist

- ✅ SECRET_KEY is secure and not exposed
- ✅ DEBUG is set to False
- ✅ ALLOWED_HOSTS is properly configured
- ✅ CORS settings are configured
- ✅ SSL/HTTPS is enabled
- ✅ Database credentials are secure
- ✅ Rate limiting is enabled

## API Documentation

- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/
- OpenAPI Schema: http://localhost:8000/schema/

## Testing

```bash
# Run tests (when implemented)
python manage.py test

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## GitHub Repository

## github repo  go to https://github.com/akfaqih3/eduak-backend




