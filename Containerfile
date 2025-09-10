FROM python:3-alpine

WORKDIR /app
COPY server /app
ENV PATH="/app/.venv/bin:$PATH"

RUN pip install -r requirements.txt

CMD uvicorn main:APP --host 0.0.0.0 --port $PORT
