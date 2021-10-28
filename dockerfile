FROM python:3.8

COPY . /app
RUN pip install  pipenv
WORKDIR /app

# install everything outside of the virtual environment

RUN pipenv install --system --deploy

CMD ["python","app.py"]
