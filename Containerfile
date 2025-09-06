FROM python:3-alpine
WORKDIR /usr/src/pivert-server
COPY server .
COPY pyproject.toml .

RUN pip install -e .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
