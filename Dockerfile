FROM python:3.10-slim-buster

RUN mkdir /app

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .


CMD ["uvicorn", "app:app", "--host=0.0.0.0"]
