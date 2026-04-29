FROM python:3.11-slim

WORKDIR /srv/mimoforge

COPY pyproject.toml README.md ./
COPY app ./app
COPY docs ./docs
COPY tests ./tests
COPY data ./data

RUN pip install --no-cache-dir .

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

