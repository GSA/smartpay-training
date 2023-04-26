# GSA SmartPay Training

This will be the quiz platform for GSA SmartPay training for card holders and AOs.

## Getting Started

### Environment Settings

There are several configuration settings that are needed. See `.env_example` for a list of environment variables that we will need. The settings object in `training/config` will try to read these from a `.env` file (which should not be checked into GitHub).

To make this work in development, create a file in the main directory called `.env` and include the variables from `.env_example`.


### Backend Dev environment

Create and activate a Python venv, then install dependencies for the FastAPI backend:

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.dev.txt -r requirements.txt
```

### Frontend dev environment

Install NPM dependencies for the Vue frontend:

```sh
npm run build:frontend
```

### Redis and PostgreSQL

This app depends on Redis to support the temporary tokens used for verification emails. It also uses PostgreSQL as a main data store. To start up local services:

```sh
docker-compose up
# Or to run them in the background:
docker-compose up -d
```

This will start:

* A local Redis cache listening on port 6379
* A local PostgreSQL database listening on port 5432
* An Adminer instance listening on port 8432

### Migrating the database schema

Run the database migrations to build the database schema:

```
alembic upgrade head
```

### Seeding the database

To load seed data into PostgreSQL, run:

```
python -m training.database.seed
```

### Run both the frontend and backend dev servers

```sh
npm run dev
```

## Testing

To run tests with code coverage checking:

```
coverage run -m pytest
```

To view the coverage report afterwards:

```
coverage report
```

## Deployment on cloud.gov

Follow these steps to deploy the application on cloud.gov.

### Bootstrap the cloud.gov environment

Before the first deployment, you need to run the bootstrap script, where `SPACE` is one of `dev`, `staging`, or `prod`. This will create all the necessary services that are required to deploy the app in that space.

```
bin/cg-bootstrap-space.sh SPACE
```

You can monitor the services deployment status with `cf services`. It can take quite a while to fully provision everything. Once the services are ready, you can bootstrap the application:

```
bin/cg-bootstrap-app.sh SPACE
```


### Create cloud.gov service accounts

Create a service account for each space. These accounts will be used by GitHub Actions to deploy the app.

```
bin/cg-service-account-create.sh SPACE
```

Take note of the username and password it creates for each space.


### Configure the GitHub environments

1. [Create environments in the GitHub repository](https://github.com/GSA/smartpay-training/settings/environments) that correspond with each space (i.e., `dev`, `staging`, and `prod`)
2. Within each GitHub environment, configure:
    * The app's secrets
        * `CG_USERNAME`: The service account username for this space
        * `CG_PASSWORD`: The service account password for this space
        * `JWT_SECRET`: A randomly generated string
        * `SMTP_PASSWORD`: Password for the SMTP relay server
    * The app's environment variables (see `.env_example` for a full list of necessary variables)


### Confirm GitHub Actions are working

At this point, GitHub Actions should be able to deploy to all configured environments.
