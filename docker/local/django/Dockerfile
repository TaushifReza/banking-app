FROM docker.io/python:3.12.2-slim-bookworm AS python

# Stage 1: Build our dependency wheels
FROM python AS python-build-stage

ARG BUILD_ENVIROMENT=local

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev

COPY ./requirements .

RUN pip wheel --wheel-dir /usr/src/app/wheels \
    -r ${BUILD_ENVIROMENT}.txt

# Stage 2 : Run Stage
FROM python AS python-run-stage

ARG BUILD_ENVIROMENT=local

ARG APP_HOME=/app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONBUFFERED=1 \
    BUILD_ENV=${BUILD_ENVIROMENT}

WORKDIR ${APP_HOME}

RUN apt-get update && apt-get install --no-install-recommends -y \
    sudo git bash-completion nano ssh \
    libpq-dev gettext \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

RUN addgroup --system django && \
    adduser --system --ingroup django django && \
    mkdir -p ${APP_HOME}/staticfiles && \
    chown django:django ${APP_HOME}/staticfiles && \
    chmod 775 ${APP_HOME}/staticfiles

COPY --from=python-build-stage /usr/src/app/wheels /wheels/

RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
    && rm -rf /wheels/

COPY --chown=django:django ./docker/local/django/entrypoint.sh /entrypoint.sh
COPY --chown=django:django ./docker/local/django/start.sh /start.sh
COPY --chown=django:django ./docker/local/django/celery/worker/start.sh /start-celeryworker.sh
COPY --chown=django:django ./docker/local/django/celery/beat/start.sh /start-celerybeat.sh
COPY --chown=django:django ./docker/local/django/celery/flower/start.sh /start-celeryflower.sh

RUN sed -i 's/\r$//g' /entrypoint.sh /start.sh /start-celeryworker.sh /start-celerybeat.sh /start-celeryflower.sh && \
    chmod +x /entrypoint.sh /start.sh /start-celeryworker.sh /start-celerybeat.sh /start-celeryflower.sh

COPY --chown=django:django . ${APP_HOME}

USER django

ENTRYPOINT [ "/entrypoint.sh" ]