# fastapi-async-demo-project

Welcome to the FastApi Async Freelancing Project. Below you will find helpful instructions on how to setup the project.

**Contents**
- How to setup App
- How to start the app

# How to setup App

Follow the below guides in order to setup the application.

## Prerequisites

- Python 3.10
- PIP3
- A Python virtual environment tool of your choice
- Docker
- postgres client

## Setup Python environment

Create a virtual Python environment using the tool of your choice. For this guide we'll use `pipenv`.
```
pipenv shell
```

Install dependencies:
```
pip install -r src/app/requirements.txt
```

## How to setup PostGreSQL DB using Docker

Follow these steps to setup the PostgreSQL DB in a container for local development:

Pull the Docker image
```
docker pull postgres
```

Start the container
```
docker run --name my-postgres -e POSTGRES_PASSWORD=secret -p 5432:5432 -d postgres
```

Check if it is running
```
docker ps
```

Connect to the database
```
psql -h localhost -p 5432 -U postgres -d postgres
```

Create the database we are going to use:
```
CREATE DATABASE app;
```

## How to setup Redis using Docker

Follow these steps to setup the Redis in a container for local development:

Pull the image
```
docker pull redis
```

Start the container
```
docker run --name my-redis-container -p 6379:6379 -d redis
```

## Setup local enviroment file

Now that the database is set up you need to add the proper variables to `src/app/.env` file:

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

Use the included `.env.example` file.

## How to run migrations using alembic

Run the `migrate.sh` script in the `src/app` folder. Alternatively you can do:
```
alembic upgrade head
```

**Note**: Make sure the project is in the Python path.

## (Optional) How to setup pgadmin using Docker

Follow these steps to setup the pgAdmin in a container for local debugging:

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


# How to start the app

This part assumes you've gone through the app setup process. To start the app, activate your Python environment and run the `start.sh` script in the root folder.

- Navigate to http://localhost:5050.
- For Swagger Docs to http://localhost:5050/docs.
