# GSA SmartPay Training

This will the quiz platform for GSA SmartPay training for card holders and AOs.

# Getting Started

## Environment Settings

## SMTP Settings
There are several configuration settings that are needed for setting emails. See .env_example for what we will (probably) need.

## JWT Secret
The backend uses a JWT (JSON Web Token) to allow the browser to tell the backend who is taking a quiz. This requires a secret key to sign the token. The settings object in `training/api/config` will try to read this from a .env file (which should not be checked into github). To make this work in development, create a file in the main directory called `.env` and add the line:

```
JWT_SECRET="some_super_secret"
```

## Backend Dev environment

``` sh
# Create and activate a Python venv
python -m venv .venv
source .venv/bin/activate
# Install dependencies
pip install -r requirements.dev.txt -r requirements.txt
# Run the local dev server
uvicorn training.main:app --reload
```

## Redis and PostgreSQL

This app depends on Redis to support the temporary tokens used for tests. It also uses PostgreSQL as a main data store. To start up local services:

``` sh
docker-compose up
```

This will start:

* A local Redis cache listening on port 6379
* A local PostgreSQL database listening on port 5432
* An Adminer instance listening on port 8432

### Seeding the database

To load seed data into PostgreSQL, run:

```
python -m training.database.seed
```

## VueJS Interface
To run view locally:
```
cd smartpay-training-quiz
npm install
npm run dev
```

# Deployment

Follow these steps to deploy the application on cloud.gov.

## Prepare the cloud.gov space

Configure cloud.gov to [permit egress from the app's space](https://cloud.gov/docs/management/space-egress/) to other services. Replace `ORG_NAME` and `SPACE_NAME` with the appropriate names for your environment:

```
cf bind-security-group trusted_local_networks_egress ORG_NAME --space SPACE_NAME
cf bind-security-group public_networks_egress ORG_NAME --space SPACE_NAME
```

The `trusted_local_networks_egress` security group allows the app to connect to cloud.gov marketplace services such as Redis and RDS. The `public_networks_egress` security group allows the app to connect to external SMTP servers.

## Provision the backend services

The API uses Redis and PostgreSQL. To provision these services on cloud.gov:

```
cf create-service aws-elasticache-redis redis-3node smartpay-training-redis
cf create-service aws-rds small-psql smartpay-training-db
```

You can monitor the deployment status with `cf services`. It might take a while to fully provision everything.

## Set up required secrets

Create a user-provided service to store secrets [in accordance with cloud.gov practices](https://cloud.gov/docs/deployment/production-ready/#protect-access-to-sensitive-credentials).

The CLI will prompt you to enter each secret one by one:

```
cf cups smartpay-training-secrets -p "JWT_SECRET, SMTP_PASSWORD"
```

## Deploy the app

After the services have been successfully created, deploy the training app but don't start it yet since we still have to set some environment variables:

```
cf push --no-start
```

## Set required environment variables

The app requires a number of environment variables. You only have to set them once per deployment on cloud.gov, and you can change them later with another `cf set-env` command.

Replace the example values with the appropriate ones and run:

```
cf set-env smartpay-training SMTP_USER "user@example.com"
cf set-env smartpay-training SMTP_SERVER "smtp.example.com"
cf set-env smartpay-training SMTP_PORT 587
cf set-env smartpay-training SMTP_STARTTLS true
cf set-env smartpay-training SMTP_SSL_TLS false
cf set-env smartpay-training EMAIL_FROM "user@example.com"
cf set-env smartpay-training EMAIL_FROM_NAME "GSA SmartPay"
cf set-env smartpay-training EMAIL_SUBJECT "GSA SmartPay Training"
cf set-env smartpay-training BASE_URL "https://federalist-....sites.pages.cloud.gov/site/gsa/smartpay-training/"
```

Restart the app to ensure it picks up the environment variables.

```
cf restart smartpay-training
```

# Updates

## App

You can deploy any updates by simply pushing the app to cloud.gov again:

```
cf push
```

## Secrets

You can update secrets by updating the user-provided service. Note that you will need to enter each secret one by one again.

```
cf uups smartpay-training-secrets -p "JWT_SECRET, SMTP_PASSWORD"
```

## Environment variables

You can update environment variables simply by setting them again. For example:

```
cf set-env smartpay-training SMTP_USER "hello@example.com"
```
