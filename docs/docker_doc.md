# [Task 1](/docs/task1.md#dependencies) / Docker container

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
## Table of Contents

- [File structure](#file-structure)
- [Files](#files)
- [Docker-Compose files](#docker-compose-files)
- [Commands](#commands)
  - [Production](#production)
  - [Tests](#tests)
- [Services](#services)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

Docker is used to have an isolated development environment and to run the project without having to install dependencies on the host machine, ensuring that the project runs the same way on any machine.

## File structure

```bash
.
├── docker/
│   ├── prod/
│   │   ├── nginx/
│   │   │   ├── Dockerfile
│   │   │   └── nginx.conf
│   │   ├── entrypoint.sh
│   │   └── Dockerfile
│   ├── test/
│   │   └── Dockerfile
│   ├── .env.db
│   └── wait-for-it.sh
├── docker-compose.yml
├── docker-compose-test.yml
└── .dockerignore
```

## Files

- `docker/prod/`: Directory that contains the necessary files for creating the production container.
- `docker/prod/nginx/`: Directory that contains the necessary files for configuring nginx.
- `docker/prod/Dockerfile`: File that contains the instructions for creating the production container.
- `docker/test/Dockerfile`: File that contains the instructions for creating the test container.
- `.env.db`: File that contains the environment variables needed for database connection.
- `wait-for-it.sh`: Script used to wait for the database to be available.

## Docker-Compose files

- `docker-compose.yml`: File that contains the configuration for creating the production containers.
- `docker-compose-test.yml`: File that contains the configuration for creating the test containers.

Both files load the environment variables from the `env` file and mount the necessary volumes.

## Commands

- `make shell`: Enters the container.
- `make migrate`: Executes the migrations.
- `make migrations`: Creates the migrations.

### Production

- `make build`: Builds the container image.
- `make build_clean`: Builds the container image without cache.
- `make up`: Starts the container.
- `make stop`: Stops the container.

See more about the [production environment](/docs/production.md).

### Tests

- `make build-test`: Builds the container image.
- `make test`: Starts the container.

## Services

- `backend`: Container that contains the application.
- `postgres`: Container that contains the database.
- `worker`: Container that contains the worker with celery.
- `redis`: Container that contains the queue server.
- `nginx`: Container that contains the web server.
