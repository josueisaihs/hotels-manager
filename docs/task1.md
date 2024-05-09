# [Tech Assessment](/README.md#the-solution) / TASK 1 - Solution

TAG `task1.0`

## Description

The API provides CRUD operations for hotels and hotel chains, and is documented with Swagger and Redocs. The API has JWT authentication and access permissions for endpoints. Additionally, a message broker is used to send email notifications when a new hotel is created.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
## Table of Contents

- [Dependencies](#dependencies)
- [Quick Start Guide](#quick-start-guide)
  - [Test Development](#test-development)
  - [Production Development](#production-development)
  - [Local Development](#local-development)
    - [Requirements](#requirements)
    - [Local Steps](#local-steps)
    - [Tests](#tests)
- [Settings](#settings)
  - [Environments variables](#environments-variables)
  - [Configuration Variables](#configuration-variables)
- [Asynchronous Task](#asynchronous-task)
  - [Celery](#celery)
  - [Broker](#broker)
- [Components](#components)
  - [Endpoints](#endpoints)
  - [Models](#models)
  - [Serializers](#serializers)
  - [Views](#views)
  - [Admin](#admin)
  - [Signals](#signals)
  - [Managers](#managers)
  - [Tests and Coverage](#tests-and-coverage)
- [Business Logic](#business-logic)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Dependencies

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.0-092E20?logo=django&logoColor=green)
![Rest Framework](https://img.shields.io/badge/Django_RESTFramework-3.15-red?logo=restframework&logoColor=green)

| Dependencies                   | Version |
| -----------------------------  | ------- |
| python                         | ^3.12.0 |
| django                         | ^5.0    |
| djangorestframework            | ^3.15.1 |
| django-autoslug                | ^1.9.8  |
| django-filter                  | 21.1    |
| Pillow                         | ^9.1.0  |
| drf-yasg                       | ^1.21.7 |
| celery                         | ^5.3.6  |
| python-dotenv                  | ^1.0.1  |
| redis                          | ^5.0.3  |
| django-celery-results          | ^2.5.1  |
| djangorestframework-simplejwt  | ^5.3.1  |
| django-cors-headers            | ^4.0.0  |

### Production Group Dependencies

| Dependencies | Version |
| ------------ | ------- |
| psycopg2     | ^2.9.3  |
| gunicorn     | ^21.1.0 |

### Test Group Dependencies

| Dependencies | Version |
| ------------ | ------- |
| coverage     | ^7.4.4  |

This project use docker to manage the dependencies and services. [See more](/docs/docker_doc.md)

## Quick Start Guide

### Test Development

To run the project, you must follow the following steps.

1. Clone the repository:

    ```bash
    git clone {repository}
    ```

2. Create the `.env.test` file and add the following variables:

    ```bash
    # app/config/settings/.env.test

    DJANGO_ENV=test
    CELERY_BROKER_URL=redis://redis:6379/0
    CELERY_RESULT_BACKEND=redis://redis:6379/0
    SECRET_KEY=django-insecure-9h6wh@3vl0mnap6w8xl=t+blb6)4@bv7xvv*m3_7enw@4)xk!$
    EMAIL_NO_REPLY=no-reply@hotelsmanager.com
    DB_NAME=djangotest
    DB_USER=django
    DB_PASSWORD=local
    DB_HOST=postgres
    DB_PORT=5432
    ```

3. Create the `.env.db` file and add the following variables:

    ```bash
    # docker/.env.db

    POSTGRES_USER=django
    POSTGRES_PASSWORD=local
    POSTGRES_DB=djangotest
    ```

4. Run the tests:

    ```bash
    make build-test && make test
    ```

### Production Development

To run the project, you must follow the following steps.

Regarding the production environment, a `docker-compose.yml` file has been configured to run the project in a production environment. And a `.env.prod` file is needed to configure the environment variables, it contains the same variables as the `.env.test` file but with the production database variables.

Once the `.env.prod` file is configured, the following command should be executed:

```bash
make build && make up
```

Access the API at [http://localhost/api/v1/](http://localhost/api/v1/)

### Local Development

To run the project, you must follow the following steps. The project has been configured with `poetry` to manage the dependencies and `pyenv` to manage the python versions.

#### Requirements

- Install `poetry`:

    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```

- Install `pyenv`:

    ```bash
    brew install pyenv
    ```

#### Local Steps

1. Clone the repository:

    ```bash
    git clone {repository}
    ```

2. Create a virtual environment:

    ```bash
    pyenv install 3.8.10
    poetry env use /Users/$USER/.pyenv/versions/3.8.10/bin/python
    ```

3. Install the dependencies:

    ```bash
    poetry install
    ```

4. Create the `.env` file and add the following variables:

    ```bash
    # app/config/settings/.env
    ENV=local
    CELERY_BROKER_URL=redis://localhost:6379/0
    RESULT_BACKEND=redis://localhost:6379/0
    SECRET_KEY=django-insecure-9h6wh@3vl0mnap6w8xl=t+blb6)4@bv7xvv*m3_7enw@4)xk!$
    EMAIL_NO_REPLY=no-reply@hotelsmanager.com
    ```

5. Create the `local.py` file in the `app/config/settings/` folder and add the following variables:

    ```python
    # app/config/settings/local.py
    from .base import *

    DEBUG = True

    ALLOWED_HOSTS = ("*",)

    # Database
    # https://docs.djangoproject.com/en/5.0/ref/settings/#databases

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
    ```

6. Run the migrations:

    ```bash
    make quick-migrate
    ```

7. Create a superuser:

    ```bash
    ./manage.py createsuperuser
    ```

8. Run the server:

    ```bash
    ./manage.py runserver
    ```

9. Run the broker, use other terminal window:

    ```bash
    make broker
    ```

10. Run Celery, use other terminal window:

    ```bash
    make celery
    ```

11. Access the API at [http://localhost:8000/api/v1/](http://localhost:8000/api/v1/)

#### Tests

To run the tests, you must run the following command:

```bash
./manage.py test
```

## Settings

The configuration is loaded through the files inside the `app/config/settings/` folder and they are separated by environments. To run the project in a specific environment, you should execute the following command:

```bash
./manage.py runserver --settings=app.config.settings.{environment}
```

The project has been configured to have four execution environments:

- `test`: Testing environment
- `prod`: Production environment

The main configuration of the project is in the file `app/config/settings/base.py`.

### Environments variables

Each of them corresponds to a `.env{.enviroment}` file in the `app/config/settings/` folder with the corresponding environment variables. The variables to configure are as follows:

| Variable              | Description       |
| -----------------     | -----------       |
| DJANGO_ENV            | Environment       |
| SECRET_KEY            | Django secret key |
| CELERY_BROKER_URL     | Allowed hosts     |
| CELERY_RESULT_BACKEND | Database URL      |
| EMAIL_NO_REPLY        | Email host        |
| DB_NAME               | Database name     |
| DB_USER               | Database user     |
| DB_PASSWORD           | Database password |
| DB_PORT               | Database port host |
| DB_HOST               | Database port host |

To configure the database service, you need to create a `.env.db` file in the `docker/` folder with the following variables:

| Variable              | Description       |
| -----------------     | -----------       |
| POSTGRES_DB           | Database name     |
| POSTGRES_USER         | Database user     |
| POSTGRES_PASSWORD     | Database password |

### Configuration Variables

The project has a configuration file `app/config/settings/base.py` where the some following variables are defined:

- `REST_FRAMEWORK`: Configuration of the Django Rest Framework. [More info](https://www.django-rest-framework.org/api-guide/settings/)
  - `DEFAULT_PERMISSION_CLASSES`: Default permissions for the API, only authenticated users can access
  - `DEFAULT_AUTHENTICATION_CLASSES`: Default authentication for the API, JWT

- `SIMPLE_JWT`: Configuration of the Django Rest Framework Simple JWT. [More info](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html)
  - `ACCESS_TOKEN_LIFETIME`: Lifetime of the access token, default 5 minutes
  - `REFRESH_TOKEN_LIFETIME`: Lifetime of the refresh token, default 1 day

- Celery configuration. [More info](https://docs.celeryproject.org/en/stable/userguide/configuration.html)
  - `CELERY_BROKER_URL`: URL of the message broker
  - `CELERY_RESULT_BACKEND`: URL of the database to store the results of the tasks

- Special chains. List of words that define a special hotel chain.
  - `SPECIAL_CHAINS`: List of words that define a special hotel chain.

    ```python
    SPECIAL_CHAINS = [
        {"name": "Four seasons", "email": "four-seasons@hotelsmanager.com"},
    ]
    ```

- Email configuration. [More info](https://docs.djangoproject.com/en/5.0/topics/email/#email-backends)
  - `EMAIL_NO_REPLY`: Email to send notifications

## Asynchronous Task

### Celery

Celery has been configured to queue tasks. To run Celery, you must run the following command:

```bash
make celery
```

### Broker

Broker has been configured for Celery. To run it, you must run the following command:

```bash
make broker
```

Note that you must modify the `make` file with the command of your messaging broker. By default, Redis has been configured and has also been installed in the python environment.

## Components

### Endpoints

The API has the following endpoints:

- `/admin/`: Django Admin
- `/api/v1/hotels/`: CRUD of hotels
- `/api/v1/hotelchains/`: CRUD of hotel chains

- Auto documentation
  - `/api/v1/`: Swagger
  - `/api/v1/redocs/`: Redocs

- JWT
  - `/api/v1/token/`: Obtain token
  - `/api/v1/token/refresh/`: Refresh token
  - `/api/v1/token/verify/`: Verify token

For more information on the API endpoints, you can access the API documentation at `/api/v1/redoc`.

### Models

Models have been defined for the API:

- `Hotel`: Model to store hotel information
- `HotelChain`: Model to store hotel chain information

### Serializers

Serializers have been defined for the API models:

- `HotelSerializer`: Serializer for the model `Hotel`
- `HotelChainSerializer`: Serializer for the model `HotelChain`

### Views

Views have been defined for the API models:

- `HotelViewSet`: View for the `Hotel` model
- `HotelChainViewSet`: View for the `HotelChain` model

### Admin

Admins have been defined for the API models:

- `HotelAdmin`: Admin for the model `Hotel`
- `HotelChainAdmin`: Admin for the model `HotelChain`

### Signals

Signal handlers have been defined for the API models:

- `assign_special_chain_case_and_send_mail`: Signal to send an email notification to the chain when a new hotel is created if the hotel chain is special
- `hotel_related_hotels`: Signal to relate hotels according to the business logic
- `title_format`: Signal to format the title of the hotel chain before saving it

### Managers

Mangers have been defined for the API models:

- `HotelManager`: Manager for the `Hotel` model
  - `get_resorts`: Method to get hotels related to other hotels with the word "resort" in the title
  - `nested_create`: Method to create hotels with nested hotel chains.

- `HotelChainManager`: Manager for the `HotelChain` model
  - `create`: Method to create a hotel chain and keep the `title` field unique.

### Tests and Coverage

Test have been defined for the API models, serializers, and views. To run the tests, you must run the following command:

```bash
./manage.py test
```

To generate the coverage report, you must run the following command:

```bash
make coverage-report
```

## Business Logic

The business logic of the API is as follows:

1. A hotel can belong to only one hotel chain or not belong to any hotel chain.
2. A hotel chain can be special if its title contains certain words configured in the `SETTINGS.SPECIAL_CHAINS` variable.
3. A hotel is assigned to a hotel chain if its title contains certain words configured in the `SETTINGS.SPECIAL_CHAINS` variable.
    - If the chain does not exist, a new hotel chain is created.
4. An email notification is sent to the hotel chain when a new hotel is created if the hotel chain is special.
5. A hotel is related to other hotels if its title contains the word "resort".
6. A hotel can only be created even if it does not belong to any hotel chain.
7. A hotel chain is created if its title is unique, otherwise the existing hotel chain is returned.
8. The title of a hotel chain is formatted as `title` before saving it. Example: "hotel chain", "HoTel ChAiN" -> "Hotel Chain"

Also see:
[Task 1.1](/docs/task1.1.md)

---

[Back to Top](#table-of-contents)

<!--
Notes

Comment `# region NAME` is used to group the code into sections and facilitate reading the code. To collapse the sections, you must install the `Better Comments` extension in Visual Studio Code. And also marks the region on the editor minimap.

Comment `# type: ignore` is used to ignore typing errors in the code.
-->
