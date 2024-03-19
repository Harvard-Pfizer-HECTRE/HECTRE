# HECTRE API APP

## Poetry

```bash
poetry install
```

## Makefile

```bash
make dev # run uvicorn with restart
make test # run pytest
make create-items # create items for illustration purposes
make get-items # retrieve items for illustration purposes
```

## How to install poetry

Checkout the [poetry documentation](https://python-poetry.org/docs/#installing-with-the-official-installer)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

## Alternatively you can run the app using uvicorn

First install the dependencies using pip

```bash
pip install -r requirements.txt
```

Then run the app using uvicorn

```bash
uvicorn app.main:app --reload
```
