FROM python:3.8

COPY . /app
RUN pip install  pipenv
WORKDIR /app

ENV FLASK_APP=app.py

# install everything outside of the virtual environment
RUN pipenv install --system --deploy

RUN pip install uwsgi


CMD ["uwsgi", "wsgi.ini"]


