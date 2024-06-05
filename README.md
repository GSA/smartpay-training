# GSA SmartPay Training

This will be the quiz platform for GSA SmartPay training for card holders and AOs.

## Setting up for development and testing
  
### Environment variable settings
This application requires several configuration settings that are pulled from a file called `.env`. We do not check this file into the Github repo. Instead, we provide a template at [`.env_example`](/.env_example).
  
You should create a new `.env` file locally in the root of the repository, copying the template and updating values per the instructions below.
  
#### Setting up email
This application requires an SMTP service for sending confirmation emails when signing up for training. This means we need to provide corresponding variable values so that, when in development mode, we can receive test emails.
 
We recommend using [Ethereal](https://ethereal.email/) to set up an easy to use, temporary, free email account. When you create an account there, Ethereal will provide you with a username, password, an SMTP address, and an SMTP port. You should update your copied `.env` file with the corresponding values (updating with the values Ethereal gets you):
```config
SMTP_SERVER="<etheral-smtp-server-address>"
SMTP_PORT=<ethereal-smtp-server-port>
  
SMTP_PASSWORD="<ethereal-account-password>"
SMTP_USER="<ethereal-account-email-address>"
```
  
#### Update the base url
For development, we need to update the `BASE_URL` environment value so that confirmation emails link back to the locally running application. By default, our web application will be running locally at port `4321` when in development:
```config
BASE_URL="http://localhost:4321"
```
**Note the lack of a trailing slash!**

### Service dependencies

This app depends on a few services. For local development, these services have been neatly packaged into a Docker Compose stack. First, optionally edit `dev/uaa/uaa.yml` to create your own test user accounts (see the `scim.users` section of that file). Then to run the services:

```sh
docker-compose up -d
```

This will start:

* A local UAA instance listening on port 8080
* A local Redis cache listening on port 6379
* A local PostgreSQL database listening on port 5432
* An Adminer instance listening on port 8432


### Python environment settings
The backend uses Python and FastAPI. You will want to set up a virtual environment for installing python packages locally. To set one up and install the needed dependencies, run the following:

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.dev.txt -r requirements.txt
```

### Frontend environment settings
The frontend is built using [Astro](https://astro.build/) and [Vue](https://vuejs.org/). These require an installation of Node. We recommend using one of the following development environments for Node:
* [NVM](https://github.com/nvm-sh/nvm) -- The correct Node version is set automatically from this repo's `.nvmrc` file (Node LTS v18)
* [nodeenv](https://pypi.org/project/nodeenv/), which is compatible with python's virtualenv. If you use this option, be sure to use the latest Node LTS version, which is `v18`.
  
  
  
Once you have a proper Node environment set up, you can install the frontend dependencies as follows:

```sh
npm run build:frontend
```

### Database setup and migrating the schema
With your database service running in Docker (see [this section](#service-dependencies) for setting that up), you will need to run the necessary database migrations and seed the database with initial data.
  
**IMPORTANT**: If you have `postgres` already running locally on your machine as a service, you will want to disable it. The Docker version of the database runs at the default `postgres` port, but your local version will take priority and the scripts could fail if it's running. You'll know if you see errors about not having a user called `postgres` or similar.

#### Running Migrations

We use [Alembic](https://alembic.sqlalchemy.org/en/latest/) to run the database migrations. If you installed the python environment according to the earlier instructions, it should already be available to you.
  
To run the migrations:

```
alembic upgrade head
```

#### Seeding the database

To load seed data into PostgreSQL, run:

```
python -m training.database.seed
```

#### Importing training questions into the db
In order to fully use the application in development, we will need to import the training quizzes into the database. However, _we do not commit that data to this repository_. You will need to contact the project maintainers to get access to the training quiz data sql dump file.
  
Once you have that file, you can run the following to import quiz data into the db:
```
# Assuming the dump file is named quiz-data-dump.sql
psql -h localhost -p 5432 -U postgres -W postgres < /path/to/quiz-data-dump.sql
```

## Running in development
First, be sure you have followed all the [instructions for setting up for development](#setting-up-for-development-and-testing).
  
To run both the python backend and the frontend at the same time, execute:

```sh
npm run dev
```

## Testing
Before attempting to run tests, be sure that you have followed all the [instructions for setting up for development](#setting-up-for-development-and-testing).
  
### Backend tests (python)
  
To run tests with code coverage checking:

```shell
coverage run -m pytest
```

To view the coverage report afterwards:

```shell
coverage report
```
  
To run python tests showing the location of any skipped tests:
```shell
pytest -r fEs
```

### Frontend tests (node/javascript)
To run the frontend tests, execute
```shell
cd training-frontend
npm run test:coverage
```

## Deployment on cloud.gov

Follow these steps to deploy the application on cloud.gov. Your cloud.gov account must have the `SpaceDeveloper` role in each space in order to run these scripts.

### Bootstrap the cloud.gov environment

Before the first deployment, you need to run the bootstrap script, where `SPACE` is one of `dev`, `test`, `staging`, or `prod`. This will create all the necessary services that are required to deploy the app in that space.

```
bin/cg-bootstrap-space.sh SPACE
```

You can monitor the services deployment status with `cf services`. It can take quite a while to fully provision everything. Once the services are ready, you can bootstrap the application:

```
bin/cg-bootstrap-app.sh SPACE
```


### Create cloud.gov service accounts

Create a service account for each space. These accounts will be used by GitHub Actions to deploy the app. Since we are currently manually deploying to the `test` space, we do not need a service account for that space.

```
bin/cg-service-account-create.sh SPACE
```

Take note of the username and password it creates for each space.


### Configure the GitHub environments

1. [Create environments in the GitHub repository](https://github.com/GSA/smartpay-training/settings/environments) that correspond with each space that GitHub Actions will deploy to (i.e., `dev`, `staging`, and `prod`)
2. Within each GitHub environment, configure:
    * The app's secrets
        * `CG_USERNAME`: The service account username for this space
        * `CG_PASSWORD`: The service account password for this space
        * `JWT_SECRET`: A randomly generated string
        * `SMTP_PASSWORD`: Password for the SMTP relay server (optional depending on the SMTP server being used)
    * The app's environment variables (see `.env_example` for a full list of necessary variables)


### Confirm GitHub Actions are working

At this point, GitHub Actions should be able to deploy to all configured environments.

### Notes for the test space

We treat the `test` space differently:

* We configure and push to it manually and not via GitHub Actions, which allows us to customize the space a bit for user testing
* You can bootstrap the `test` space following the space and app bootstrap steps above, but the `test` space does not need a service account
* You need to set the environment variables and secrets yourself using the `bin/cg-set-env.sh` and `bin/cg-set-secret.sh` scripts rather than configuring them via GitHub environments
* You need to run the database migrations and database seed using `cf run-task`
