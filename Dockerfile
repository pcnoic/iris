FROM ubuntu:latest
LABEL Maintainer="Christos Alexiou <christos@tynr.io>"

RUN apt update -y && apt upgrade -y

RUN apt install -y -q build-essential python3-pip python3-dev
RUN pip3 install -U pip setuptools wheel
RUN pip3 install gunicorn uvloop httptools

COPY requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt

COPY src/ /app

EXPOSE 80
WORKDIR /app

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:80", "--workers", "1" ,"--threads", "8", "--timeout", "0" ,"api:app"]
