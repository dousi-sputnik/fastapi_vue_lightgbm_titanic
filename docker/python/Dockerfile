FROM python:3.11

COPY ./docker/python/requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /app

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
