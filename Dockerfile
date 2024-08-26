
FROM python:3.11-slim as builder

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

COPY . .

FROM python:3.10-slim

WORKDIR /app
COPY --from=builder /app /app

EXPOSE 8080

# Set the entry point to run the Pulumi scripts
CMD ["poetry", "run", "pulumi-gcp"]