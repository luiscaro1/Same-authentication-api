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

To add a new dependency to the project use the following command in the project's root directory:

<br/>

```
pipenv install <package name>
```

<br/>

## Running Development

<br/>
To run the project write the following command in the project's root directory:
<br/>
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
