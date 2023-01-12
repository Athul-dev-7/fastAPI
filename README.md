# FastAPI-App

This is a sample FastAPI CRUD application that uses a PostgreSQL database.

## To run the application locally

### Requirements

-   Python 3.8 or higher
-   PostgreSQL 12 or higher

### Installation

#### 1. Clone the repository:

`git clone https://github.com/Athul-dev-7/fastAPI.git`

#### 2. Move to the project's root directory:

`cd fastAPI`

#### 3. Create a virtual environment and activate it:

`python3 -m venv venv`

`source venv/bin/activate`

#### 4. Install the requirements:

`pip install -r requirements.txt`

#### 5. Set up the database:

-   To install PostgreSQL on Ubuntu, you can follow these steps:

    -   1.  Update the package manager's package list:

            `sudo apt update`

    -   2.  Install the PostgreSQL package:

            `sudo apt install postgresql postgresql-contrib`

            This will install PostgreSQL and some additional utilities.

    -   3.  After the installation is complete, the PostgreSQL service will be started automatically. You can check the status of the service by running:

            `systemctl status postgresql`

    -   4.  By default, PostgreSQL creates a user named `postgres` with the role `postgres`. You can connect to the PostgreSQL server as this user by running:

            `sudo su - postgres`

    -   5.  Once you are connected to the PostgreSQL server, you can create new user and database.

-   ADD _.env_ file at the root of the project directory and edit these fields according to your database config:

    -   DATABASE_HOST_NAME=
    -   DATABASE_PORT=
    -   DATABASE_NAME=
    -   DATABASE_USERNAME=
    -   DATABASE_PASSWORD=
    -   SECRET_KEY=
    -   ALGORITHM=
    -   ACCESS_TOKEN_EXPIRE_MINUTES=

-   Run the following command to apply the database migrations:

`alembic upgrade head`

#### 6. Start the application:

`uvicorn main.app:app --reload`

The application will be available at http://localhost:8000.

## To run the application in a Docker container

### Requirements

-   Docker
-   Docker Compose

### Steps

-   Once installed the above 2 requirements, go to the project's root directory containing both _Dockerfile_ & _docker-compose.yaml_ files and run this command:

    `sudo docker-compose up --build -d`

-   Once container is up, Please follow these commands

-   To list the running containers:

    -   `sudo docker-compose ps`

-   To migrate database using alembic

    -   `sudo docker-compose exec -it api bash`

    -   `alembic upgrade head`

-   To down the container
    -   `docker-compose down` to down the container
