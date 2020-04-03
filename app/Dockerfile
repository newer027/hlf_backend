# pull official base image
FROM python:3.6.4-alpine3.7

# set work directory
WORKDIR /usr/src/app

# set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories

RUN echo "[global]"$'\r'"trusted-host =  mirrors.aliyun.com"$'\r'"index-url = http://mirrors.aliyun.com/pypi/simple" > /etc/pip.conf

ENV PYTHONIOENCODING=utf-8

# install psycopg2
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk del build-deps

# install dependencies
RUN pip install --upgrade pip
RUN pip install pipenv
COPY ./Pipfile /usr/src/app/Pipfile
RUN pipenv install --skip-lock --system --dev

# copy entrypoint
COPY ./run_django.sh /usr/src/app/run_django.sh

# copy project
COPY . /usr/src/app/

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/run_django.sh"]
