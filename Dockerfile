FROM --platform=linux/amd64 python:3.9.16-slim-bullseye
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE ${CONFIG_PORT}
CMD [ "python3", "application.py" ]

RUN pip install newrelic

ENV NEW_RELIC_APP_NAME="aws-bytecloud"
ENV NEW_RELIC_LOG=stdout
ENV NEW_RELIC_DISTRIBUTED_TRACING_ENABLED=true
ENV NEW_RELIC_LICENSE_KEY=a5a45a4b242e59d119a43a76cf587449FFFFNRAL
ENV NEW_RELIC_LOG_LEVEL=info

ENTRYPOINT [ "newrelic-admin", "run-program" ]
