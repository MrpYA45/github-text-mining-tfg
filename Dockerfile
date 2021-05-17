# syntax=docker/dockerfile:1

FROM ubuntu:latest

RUN /bin/bash -c "\
    apt update && \
    apt install -y python3 python3-pip && \
    apt clean \
    "

RUN mkdir /app

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY src/ app/

RUN find ./ -name "*.sh" -exec chmod a+x {} \;

#RUN find ./ -name "setup.py" -exec chmod a+x {} \;

RUN ./app/backend/install.sh

CMD ["./app/backend/start.sh"]
