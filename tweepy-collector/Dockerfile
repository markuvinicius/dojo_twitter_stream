FROM python:3.6
LABEL maintainer 'Marku Vinicius <markuvinicius@gmail.com>'

ENV PYTHONUNBUFFERED 1
RUN pip install tweepy && pip install pymongo

ENTRYPOINT ["/usr/local/bin/python"]