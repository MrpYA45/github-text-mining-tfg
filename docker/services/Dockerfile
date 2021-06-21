FROM ubuntu:latest

RUN /bin/bash -c "\
    apt update && \
    apt install -y python3 python3-pip libmariadb-dev && \
    apt clean \
    "

ADD bootstrap.sh /app/scripts/

RUN find ./ -name "*.sh" -exec chmod a+x {} \;

ENTRYPOINT ["/app/scripts/bootstrap.sh"]
