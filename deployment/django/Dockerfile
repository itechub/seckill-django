FROM python:3.7-alpine

RUN apk add --no-cache jpeg-dev zlib-dev mysql-dev
RUN pip3 install virtualenv

RUN virtualenv /env
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH
# Copy requirements.pip in advance
ADD ./requirements.txt /env/app/requirements.txt

WORKDIR /env/app

RUN apk add --no-cache --virtual .build-deps build-base linux-headers \
    && pip install -r requirements.txt \
    && apk del .build-deps

COPY ./deployment/django/docker-entrypoint.sh  /env/app/
RUN chmod +x /env/app/docker-entrypoint.sh

# Reading the context from the docker-compose build setting
COPY ./ /env/app

EXPOSE 8080

VOLUME ["/env/app/collectstatic/statics", "/env/app/media"]

ENTRYPOINT ["/env/app/docker-entrypoint.sh"]

CMD ["sh", "-c", "/env/bin/gunicorn --worker-class=gevent --worker-connections=1000 --workers=9 --timeout 240 --bind  0.0.0.0:8080  config.wsgi:application"]
