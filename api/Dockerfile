FROM python:3.11
WORKDIR /code

RUN pip install --no-cache-dir --upgrade fastapi uvicorn requests redis_om
COPY ./app /code/app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]