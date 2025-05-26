# Task by Mohir dev team

Task by Mohir dev team

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

License: MIT

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## LOCAL DEV:Basic Commands
- Running application locally

      $ docker-compose up --build 
    
- Making migration locally

      $ docker-compose run --rm django python manage.py makemigrations/migrate
    

- To create a **superuser account**, use this command:

      $ docker-compose run --rm django python manage.py createsuperuser

- Accessing to swagger from local browser 

      $ http://localhost:8000/api/docs/


For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy apps

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

### Celery

This app comes with Celery.

To run a celery worker:

```bash
cd apps
celery -A config.celery_app worker -l info
```

Please note: For Celery's import magic to work, it is important _where_ the celery commands are run. If you are in the same folder with _manage.py_, you should be right.

To run [periodic tasks](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html), you'll need to start the celery beat scheduler service. You can start it as a standalone process:

```bash
cd apps
celery -A config.celery_app beat
```

or you can embed the beat service inside a worker with the `-B` option (not recommended for production use):

```bash
cd apps
celery -A config.celery_app worker -B -l info
```

### Sentry

Sentry is an error logging aggregator service. You can sign up for a free account at <https://sentry.io/signup/?code=cookiecutter> or download and host it yourself.
The system is set up with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.

## Deployment
The following details how to deploy this application.
1. Run docker production file for after creating .env files for django app and portgres with names .django and .postgres in .envs/.production directory of the app

- Running application in prod mode

      $ docker-compose -f docker-compose.production.yml up --build -d
    
- Making migration in prod mode (never make migration in prod mode)

      $ docker-compose -f docker-compose.production.yml run --rm django python manage.py migrate

- To create a **superuser account**, use this command:

      $ docker-compose -f docker-compose.production.yml run --rm django python manage.py createsuperuser
    
- Accessing to swagger from your browser 

      $ https://your_domain.uz/api/docs/

2. Configure nginx for the domain and the port which app is running on.
See detailes [nginx documentation](https://nginx.org/en/docs/)

### Docker

See detailed [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).


