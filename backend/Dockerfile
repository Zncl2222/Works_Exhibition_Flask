FROM python:3.9-slim-bullseye
LABEL maintainer Zncl2222

RUN echo "deb http://opensource.nchc.org.tw/debian/ bullseye main" > /etc/apt/sources.list \
  && echo "deb http://opensource.nchc.org.tw/debian/ bullseye-updates main" >> /etc/apt/sources.list \
  && echo "deb http://opensource.nchc.org.tw/debian/ bullseye-proposed-updates main" >> /etc/apt/sources.list

RUN apt-get update && apt-get install -y --no-install-recommends\
  build-essential \
  libldap2-dev \
  libsasl2-dev \
  libpq-dev \
  libaio-dev \
  libpq5

RUN apt-get install -y wget \
  cron \
  wget \
  python3.9-dev \
  && apt-get purge -y --auto-remove \
  && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED 1
RUN mkdir /docker_api
WORKDIR /docker_api
COPY . /docker_api/
WORKDIR /docker_api/backend

RUN python -m pip install --upgrade pip
RUN pip install -r ./requirements.txt

EXPOSE 80
RUN chmod +x /docker_api/backend/docker-entrypoint.sh
CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]

