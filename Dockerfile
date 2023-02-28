FROM python:3.11-alpine
RUN apk update && apk add python3-dev \
    gcc \
    libc-dev \
    g++ \
    libffi-dev
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt