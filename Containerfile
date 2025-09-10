FROM python:3-alpine

WORKDIR /app
COPY server /app
ENV PATH="/app/.venv/bin:$PATH"

RUN pip installl -r requirements.txt

CMD uvicorn /app/main:app --host 0.0.0.0 --port $PORT
