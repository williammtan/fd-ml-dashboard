FROM python:3.9

COPY requirements.txt ./
COPY prodigy-1.11.4-cp39-cp39-linux_x86_64.whl ./
RUN pip install -r requirements.txt

ADD ./ ./
RUN chmod +x ./entrypoint.sh

ARG MIGRATE
ARG ENV
ENTRYPOINT [ "bash", "./entrypoint.sh" ]
