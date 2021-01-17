FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./requirements.txt .

run pip install -r requirements.txt

COPY . /app

EXPOSE 8080