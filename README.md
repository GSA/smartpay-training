# GSA SmartPay Training

This will the quiz platform for GSA SmartPay training for card holders and AOs.

# Getting Started

## Environment Settings

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

## Redis

This needs depends on Redis to support the temporary tokens used for tests. To start up a local redis server:

``` sh
> docker-compose up
```
This will start a local Redis cache listening on port 6379.


## VueJS Interface
To run view locally:
```
cd smartpay-training-quiz
npm install
npm run dev
```

