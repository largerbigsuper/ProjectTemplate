FROM python:3.7.0

ENV PYTHONUNBUFFERED 1

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install -r /requirements/production.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com --no-cache-dir

COPY ./compose/production/django/start /start
RUN chmod +x /start

WORKDIR /app

ADD . /app

EXPOSE 8000
# ENTRYPOINT ["/entrypoint"]
