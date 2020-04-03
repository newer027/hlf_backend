FROM python:3.6.4-alpine3.7

COPY requirements/celery_app.txt /usr/src/app/requirements/celery_app.txt

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories

RUN echo "[global]"$'\r'"trusted-host =  mirrors.aliyun.com"$'\r'"index-url = http://mirrors.aliyun.com/pypi/simple" > /etc/pip.conf

ENV PYTHONIOENCODING=utf-8

RUN pip install --upgrade pip

RUN apk update \
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add postgresql-dev \
  && pip install -r /usr/src/app/requirements/celery_app.txt \
  && apk del build-deps

WORKDIR /usr/src/app

# copy entrypoint
COPY ./run_celery.sh /usr/src/app/run_celery.sh

# copy project
COPY . /usr/src/app/

# CMD ["celery", "-A", "hello_django", "worker", "--loglevel=info"]

ENTRYPOINT ["/usr/src/app/run_celery.sh"]
