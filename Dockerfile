FROM python:3.6.4

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY . .

ENV IS_PRODUCTION 1