# CyberPunk Inventory

## Endpoints
<img width="1461" alt="Screenshot 2024-09-03 at 16 04 05" src="https://github.com/user-attachments/assets/7aa146fd-d8b5-4cff-a743-58056dc73bb5">


#### Features

- [x] Authorization and authentication with JWT (JSON Web Token)

(In order to have access to the protected endpoint, an account should be registered first.)
- [x] Protected Endpoints

#### Technologies used

- FastAPI
- PostgreSQL
- SqlAlchemy
- Docker

#### Dockerized App

```sh
docker-compose up --build --force-recreate
docker-compose exec fastapi_app alembic upgrade head
```

#### Set Up Local Env

```sh
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```


#### Run tests

```sh
pytest -s tests
```


