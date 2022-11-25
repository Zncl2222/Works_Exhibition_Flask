FROM nginx:stable AS PaaSBuilder

COPY nginx.conf /etc/nginx/nginx.conf
COPY nginx_django.conf /etc/nginx/sites-available/

RUN mkdir -p /etc/nginx/sites-enabled/\
    && ln -s /etc/nginx/sites-available/my_nginx.conf /etc/nginx/sites-enabled/

FROM python:3.10-slim-bullseye
LABEL maintainer Zncl2222

RUN echo "deb http://opensource.nchc.org.tw/debian/ bullseye main" > /etc/apt/sources.list \
  && echo "deb http://opensource.nchc.org.tw/debian/ bullseye-updates main" >> /etc/apt/sources.list \
  && echo "deb http://opensource.nchc.org.tw/debian/ bullseye-proposed-updates main" >> /etc/apt/sources.list

RUN apt-get update && apt-get install -y --no-install-recommends\
  build-essential=12.6 \
  libldap2-dev \
  libsasl2-dev \
  libpq-dev \
  libaio-dev \
  libpq5

RUN apt-get install -y wget \
  cron \
  wget \
  python3.10-dev \
  && apt-get purge -y --auto-remove \
  && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED 1
RUN mkdir /docker_api
WORKDIR /docker_api
COPY . /docker_api/

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 80
RUN chmod +x /docker_api/docker-entrypoint.sh
CMD ["nginx", "-g", "daemon off;", "uwsgi", "--ini", "uwsgi.ini"]

