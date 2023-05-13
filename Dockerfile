FROM --platform=linux/amd64 python:3.9.16-slim-bullseye
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE ${CONFIG_PORT}
CMD [ "python3", "application.py" ]
