# syntax=docker/dockerfile-upstream:master-labs

FROM python:3.12-bookworm AS build
ARG UV_EXTRA_ARGS=""
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=python/uv.lock,target=uv.lock \
    --mount=type=bind,source=python/pyproject.toml,target=pyproject.toml \
    : \
    && uv sync --no-dev --locked $UV_EXTRA_ARGS \
    && :

FROM golang:1.23-bookworm AS buildgo
WORKDIR /app
RUN --mount=type=cache,target=/go/pkg/mod/ \
    --mount=type=bind,source=golang/go.sum,target=go.sum \
    --mount=type=bind,source=golang/go.mod,target=go.mod \
    --mount=type=bind,source=golang/src,target=src \
    : \
    && go mod download -x \
    && CGO_ENABLED=1 go build -o connect4img.so -buildmode=c-shared src/connect4img.go \
    && :

FROM python:3.12-slim-bookworm AS base
# https://docs.docker.com/reference/dockerfile/#copy---parents
WORKDIR /app
COPY --from=buildgo /app/connect4img.so /app/shared/
COPY --parents --from=build /app/.venv /
COPY --parents ./resources ./static ./
COPY ./python/src ./
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=0

FROM base AS production
CMD ["hypercorn", "main:app", "-b", "0.0.0.0:80"]

FROM base AS debug
COPY --parents ./scripts/readme_generator.py ./templates/README.md ./
RUN python3 scripts/readme_generator.py http://localhost/
ENV DEBUG=1
ENV LOG_LEVEL=DEBUG
CMD ["hypercorn", "main:app", "-b", "0.0.0.0:80", "--reload"]
