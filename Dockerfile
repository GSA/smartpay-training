FROM python:3.10
WORKDIR /usr/src/app
COPY requirements*.txt .
RUN pip install --no-cache-dir -r requirements.dev.txt -r requirements.txt
CMD ["uvicorn", "training.main:app", "--host", "0.0.0.0", "--reload"]
