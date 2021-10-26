FROM python:3.8-slim-buster

COPY . /app
RUN pip install  pipenv
WORKDIR /app

# install everything outside of the virtual environment

RUN pipenv install --system --deploy

CMD ["flask", "run", "-h", "0.0.0.0"]