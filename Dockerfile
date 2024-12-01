FROM python:3.11-slim

ENV PROJ_DIR='/app'
ENV PYTHONUNBUFFERED=1

RUN apt update && \
    apt install -y \
        python3-dev

WORKDIR $PROJ_DIR
COPY requirements.pip .
RUN pip3 install -r requirements.pip
COPY . /app
RUN ["chmod", "+x", "docker_entrypoint.sh"]
