# About the Project

Welcome to the backend for the GamerUp gaming forum! This project is built using Django Rest Framework and implements JWT token-based authentication. We also offer the ability to register via third-party services.

The project features a well-organized file structure and substantial unit test coverage. The code undergoes rigorous checks using the automated flake8 linter, and the testing and deployment processes are fully automated via GitHub Actions, ensuring continuous integration and delivery (CI/CD).

Additionally, Dockerfile and docker-compose are configured for the project, making it easy to launch and test the application in isolated containers.

## Installation and Launch

### Requirements

- Python 3.11+
- Git

### Installation Steps

1. Clone the repository:

```bash
git clone https://github.com/RedColdHearted/Django-GamerUp-api.git
```

2. Navigate to the project directory:

```bash
cd Django-GamerUp-api
```

3. Create a virtual environment:

```bash
python3 -m venv venv
```

4. Activate the virtual environment:

On Windows:
```bash
venv/Scripts/activate
```
On Linux:
```bash
source venv/bin/activate
```

5. Install the necessary dependencies:

```bash
pip install -r requirements.txt
```

6. If using PostgreSQL, specify the secrets in the .env file:

```env
SECRET_KEY='django-insecure-%$#14b-8=*+8z@rlh*af=)t_9#7x4$zzp)mute-vh06wt+wghp'
DJANGO_ENV='dev' # Mode of operation: dev|production

EMAIL_HOST_USER='google_mail_for_sending_emails'
EMAIL_HOST_PASSWORD='application_password'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY='authentication_key'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET='secret_key'

# For PostgreSQL connection
DB_ENGINE=django.db.backends.postgresql
DB_NAME='db_name'
DB_USER='db_user'
DB_PASSWORD='db_password'
DB_HOST='your_host'
DB_PORT='5432'
```

7. Initialize and set up the database:

```bash
python manage.py makemigrations accounts; python manage.py makemigrations posts
python manage.py migrate
```

8. Launch the application:

```bash
python manage.py runserver
```

Now the application is accessible at `http://127.0.0.1:8000/`.

## CI/CD Configuration

The following tools are used to ensure continuous integration and delivery:

- **GitHub Actions**: To automate testing and building.
- **Docker**: To containerize the application for easier deployment.
- **Railway**: A platform for deploying and hosting the application.

The repository is configured such that on each push to the main branch, tests are automatically triggered along with the linters. If successful, the deployment to Railway is performed.

## Support

If you have any questions or suggestions, please create an issue in the [Issues Section](https://github.com/REDCOLDHEARTED/FLASK-SERVICELOGIX/issues).