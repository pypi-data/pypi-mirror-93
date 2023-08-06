FROM python:3.8

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt
RUN pip install -r requirements.app

CMD uvicorn akerbp.mlops.$SERVICE_NAME.app:app --host 0.0.0.0 --port $PORT
