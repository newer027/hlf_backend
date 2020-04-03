FROM python:3.6.4-alpine3.7

COPY requirements/flower_app.txt /app/requirements/flower_app.txt

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories

RUN echo "[global]"$'\r'"trusted-host =  mirrors.aliyun.com"$'\r'"index-url = http://mirrors.aliyun.com/pypi/simple" > /etc/pip.conf

RUN pip install --upgrade pip

RUN apk update \
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add postgresql-dev \
  && pip install -r /app/requirements/flower_app.txt \
  && apk del build-deps

WORKDIR /app

COPY . /app

CMD ["celery", "-A", "hello_django", "flower", "--loglevel=info"]
