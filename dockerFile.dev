FROM python:3.8-slim-buster

COPY . /app
RUN pip install  pipenv
WORKDIR /app

RUN pipenv install --system --deploy

CMD ["flask", "run", "-h", "0.0.0.0"]