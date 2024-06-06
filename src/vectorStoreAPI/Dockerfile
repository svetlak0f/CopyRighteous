FROM --platform=linux/amd64 mirror.gcr.io/python:3.10.13-slim-bullseye

RUN apt-get update -y

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN apt-get install -y curl
COPY ./app app

CMD ["uvicorn", "app.main:app", "--port", "8000", "--host", "0.0.0.0", "--timeout-keep-alive", "600", "--forwarded-allow-ips", "*"]