# fastapi-async-demo-project

Welcome to the FastAPI Async Demo Project. Below, you will find helpful instructions on how to setup the project.

**Contents**
- Quick setup & start using docker-compose
- How to set up App manually
- How to start the App manually

# Quick setup & start using docker-compose

## Setup

This app supports docker-compose for local development.

To start the stack with Docker Compose:

```
docker-compose up
docker-compose up -d # Run as Daemon
```

**Note**:
- The first time you start your stack, it might take a minute for it to be ready as the backend waits for the database to be ready and configures everything. You can check the logs to monitor it.
- Don't forget to set up the two `.env` files. One for `docker-compose.yml`, the other for the app itself. Use the examples.

Once started, you can use the following:

- Frontend, built with Docker, with routes handled based on the path: http://localhost:8080
- Automatic interactive documentation with Swagger UI (from the OpenAPI backend): http://localhost:8080/docs
- pgAdmin, PostgreSQL web administration: http://localhost:5050


To check the logs, run:

```
docker-compose logs
```

To check the logs of a specific service, add the name of the service, e.g.:

```
docker-compose logs backend
```

If you want to start an interactive session in the backend container:

```
docker-compose exec backend bash
```

If you want to rebuild do:

```
docker-compose up --build
```

## Development

Developing using this configuration is easy because the directory with the backend code is mounted as a Docker "host volume", mapping the code you change live to the directory inside the container. That allows you to test your changes right away, without having to build the Docker image again. This should only be done during development. For production, you should build the Docker image with a recent version of the backend code. However, during development, it allows you to iterate very quickly.

Additionally, as opposed to running in production, this way of running the container starts a single server process (instead of multiple, as would be for production) and reloads the process whenever the code changes. Keep in mind that if you have a syntax error and save the Python file, it will break and exit, and the container will stop. After that, you can restart the container by fixing the error and running again.

There is also a commented-out command override. You can uncomment it and comment the default one. It makes the backend container run a process that does "nothing", but keeps the container alive. This allows you to get inside your running container and execute commands inside.

# How to set up App manually
I recommend you use docker-compose, but if for some reason you need to set up the app manually, this is the guide.

Follow the guides below in order to set up the application.

## Prerequisites

- Python 3.10
- PIP3
- A Python virtual environment tool of your choice
- Docker
- postgres client

## Set up Python environment

Create a virtual Python environment using the tool of your choice. For this guide we'll use `pipenv`.
```
pipenv shell
```

Install dependencies:
```
pip install -r src/app/requirements.txt
```

## How to set up PostgreSQL DB using Docker

Follow these steps to set up the PostgreSQL DB in a container for local development:

Pull the Docker image.
```
docker pull postgres
```

Start the container.
```
docker run --name my-postgres -e POSTGRES_PASSWORD=secret -p 5432:5432 -d postgres
```

Check if it is running.
```
docker ps
```

Connect to the database.
```
psql -h localhost -p 5432 -U postgres -d postgres
```

Create the database we will use:
```
CREATE DATABASE app;
```

## How to set up Redis using Docker

Follow these steps to set up the Redis in a container for local development:

Pull the image.
```
docker pull redis
```

Start the container.
```
docker run --name my-redis-container -p 6379:6379 -d redis
```

## Set up local enviroment file

Now that the database is set up, you need to add the proper variables to `src/app/.env` file:

```
#Backend
PROJECT_NAME=<project_name>

#Database
DB_HOST=<host:port> # e.g. localhost:5432
DB_USER=<user> # e.g. postgres
DB_PASS=<secret>
DB_NAME=<database_name>
#Cache
REDIS_HOST=<host> # e.g. localhost
```

Use the included `.env.example` file for reference.

## How to run migrations using alembic

Run the `migrate.sh` script in the `src/app` folder. Alternatively you can do:
```
alembic upgrade head
```

**Note**: Make sure the project is in the Python path.

## (Optional) How to set up pgAdmin using Docker

Follow these steps to set up the pgAdmin in a container for local debugging:

Pull the Docker image
```
docker pull dpage/pgadmin4
```

Start the container
```
docker run --name my-pgadmin -p 8080:80 -e "PGADMIN_DEFAULT_EMAIL=user@example.com" -e "PGADMIN_DEFAULT_PASSWORD=secret" -d dpage/pgadmin4
```

Access pgAdmin: Open your web browser and navigate to `localhost:8080`. You will see the pgAdmin login page.

Add a PostgreSQL Server: Once logged in, click on the "Add New Server" option in the "Quick Links" or "Dashboard" section.

In the "General" tab, provide a name for the server.
In the "Connection" tab, enter the following details:
- Host: Use the IP address of the PostgreSQL container
    - Use `docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' my-postgres` to get it.
- Port: The port on which PostgreSQL is running inside the container (e.g., 5432).
- Maintenance database: The name of the default database (e.g., postgres).
- Username: The username to connect to the PostgreSQL container (e.g., postgres).
- Password: The password for the PostgreSQL user.


# How to start the app manually

This part assumes you've gone through the app set up process. To start the app, activate your Python environment and run the `start.sh` script in the root folder.

- Navigate to http://localhost:5050.
- For Swagger Docs to http://localhost:5050/docs.
