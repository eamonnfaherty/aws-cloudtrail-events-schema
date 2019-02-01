FROM python:3.7.2-alpine3.8

RUN pip install aws-cloudtrail-events-schema

ENTRYPOINT ["/usr/local/bin/cloudtrail-schema"]