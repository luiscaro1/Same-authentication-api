# Same-authentication-api

## Initial setup

<br>

### Vritual Environment

<br/>

Run the following command to install pipenv:

<br/>

```

pip install pipenv
```

<br/>

Later, run the following command to activate the virtual environment:

<br/>

```
pipenv shell
```

<br/>

Finally, install the project's dependencies with the following:

<br/>

<br/>

```
pipenv install
```

## Installing Dependencies

<br/>

To add a new dependency to the project use the following command in the project's root directory. Make sure you have pip env installed locally and have a python 3+ version running on your computer:

<br/>

If you do not have pipenv installed locally, then do so by running the following commmand:

<br/>

```
pip install pipenv
```

Make sure you are in the development environment by running:

<br/>

```
pipenv shell
```

<br/>

Finally, install project dependencies by running:

<br/>

```
pipenv install <package name>
```

<br/>

## Running Development

<br/>

To run the project write the following command in the project's root directory:

<br/>

### Inside of the container:

<br/>

```
docker compose -f docker-compose.dev.yml up --build
```

<br/>

### Outside of the container:

<br/>

```
flask run
```
