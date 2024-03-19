# syntax=docker/dockerfile-upstream:master-labs

FROM python:3.12.0-alpine as build
WORKDIR /app
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY ./resources ./
RUN --mount=type=cache,target=/var/cache/apk/ \
    --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    : \
    && apk add gcc musl-dev linux-headers git \
    && pip install -U pip \
    && pip install -U -r requirements.txt \
    && :

FROM python:3.12.0-alpine as base
COPY --parents --from=build /opt/venv /
WORKDIR /app
COPY ./src ./
COPY --parents  ./resources ./
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=0

FROM base as production
ENV GITHUB_PROFILE_URL="https://github.com/AiroPi"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]


FROM base as debug
ENV DEBUG=1
ENV LOG_LEVEL=DEBUG
ENV GITHUB_PROFILE_URL="http://localhost/readme.md"
COPY ./readme.html ./-
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
