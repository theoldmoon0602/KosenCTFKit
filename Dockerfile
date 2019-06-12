FROM alpine:latest

RUN apk add --no-cache nodejs npm python3 python3-dev alpine-sdk libffi-dev openssl-dev  build-base jpeg-dev zlib-dev openssh-client rsync mariadb-dev
RUN npm install -g yarn
RUN pip3 install pipenv gunicorn
RUN mkdir /app
WORKDIR /app

ADD Pipfile.lock /app/Pipfile.lock
ADD Pipfile /app/Pipfile
ADD package.json /app/package.json
ADD yarn.lock /app/yarn.lock

RUN pipenv install --system
RUN yarn install --production=false

ADD kosenctfkit /app/kosenctfkit
ADD src /app/src
ADD static /app/static

ENV PARCEL_WORKERS=1
RUN yarn build

ADD app.py /app/app.py
ADD manage.py /app/manage.py
ADD ssh /root/.ssh
RUN chmod -R 0600 /root/.ssh
