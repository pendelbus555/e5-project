FROM python:3.10.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/e5_site

COPY ../requirements.txt .
RUN pip install -r requirements.txt

COPY . .