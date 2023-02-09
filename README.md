# GSA SmartPay Training

This will be the backend of a quiz platform for GSA SmartPay training for card holders and AOs.

# Getting Started

## Dev environment

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
