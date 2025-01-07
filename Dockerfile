# syntax=docker/dockerfile-upstream:master-labs

FROM python:3.12-alpine AS build
ARG EXTRA_DEBUG=""
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
WORKDIR /app
RUN --mount=type=cache,target=/var/cache/apk \
    --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    : \
    && apk update && apk add gcc musl-dev linux-headers git  \
    && uv sync --no-dev --locked $EXTRA_DEBUG \
    && :

FROM python:3.12-alpine AS base
# https://docs.docker.com/reference/dockerfile/#copy---parents
WORKDIR /app
COPY --parents --from=build /app/.venv /
COPY --parents ./resources ./
COPY ./src ./
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=0

FROM base AS production
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

FROM base AS debug
COPY ./debug_pages /app/debug_pages
ENV DEBUG=1
ENV LOG_LEVEL=DEBUG
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
