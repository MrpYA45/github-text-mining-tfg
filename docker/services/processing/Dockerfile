FROM ubuntu:latest

RUN /bin/bash -c "\
    apt update && \
    apt install -y python3 python3-pip libmariadb-dev && \
    apt clean \
    "

RUN pip3 install torch transformers[torch]

ADD bootstrap.sh /app/scripts/

RUN find ./ -name "*.sh" -exec chmod a+x {} \;

ENTRYPOINT ["/app/scripts/bootstrap.sh"]
