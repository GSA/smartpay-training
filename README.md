# GSA SmartPay Training

This will be the backend of a quiz platform for GSA SmartPay training for card holders and AOs.

# Getting Started
This needs depends on Redis to support the temporary tokens used for tests. To start up a local redis server:

``` sh
> docker-compose up
```
This will start a local Redis cache listening on port 6379.

# Environment Settings

## JWT Secret
The backend uses a JWT (JSON Web Token) to allow the browser to tell the backend who is taking a quiz. This requires a secret key to sign the token. The settings object in `training/api/config` will try to read this from a .env file (which should not be checked into github). To make this work in development, create a file in the main directory called `.env` and add the line:

```
JWT_SECRET="some_super_secret"
```

# API 
To run the API locally:

Create venv to isolate dependencies and install dependencies
 ``` sh
 python -m venv .venv
 pip install -r requirements.txt
 pip install -r requirements.dev.txt
 ```

Run app with uvicorn or similar:
``` sh
uvicorn training.main:app
```

if it's working you should see life-affirming messages like:
>  Uvicorn running on http://127.0.0.1:8000 

# VueJS Interface
To run view locally:
```
cd smartpay-training-quiz
npm install
npm run dev
```

It should confim it's running with a message like:
> VITE v4.1.1  ready in 789 ms  
>      ➜  Local:   http://127.0.0.1:5173/