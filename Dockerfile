FROM ubuntu:latest
LABEL Maintainer="Christos Alexiou <christos@tynr.io>"
ARG project_name


RUN apt update -y && apt upgrade -y

RUN apt install -y -q build-essential python3-pip python3-dev
RUN pip3 install -U pip setuptools wheel
RUN pip3 install gunicorn uvloop httptools

COPY requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt

COPY src/ /app
COPY credentials/${project_name}/firebase_private_key.json /app/firebase_private_key.json

EXPOSE 80
WORKDIR /app

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:80", "--workers", "1" ,"--threads", "8", "--timeout", "0" ,"api:app"]
