# syntax=docker/dockerfile:1.4

# Build stage
FROM python:3.10-bookworm AS build

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN <<EOF
    pip install wheel
    pip install -r requirements.txt
EOF

# Final stage
FROM python:3.10-slim-bookworm

COPY --from=build /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN <<EOF
  mkdir -p /opt/airflow/dags
  mkdir -p /opt/airflow/logs
EOF

ENV AIRFLOW_HOME="/opt/airflow"

COPY <<-EOF /opt/airflow/webserver_config.py
AUTH_ROLE_PUBLIC = "Admin"
EOF

WORKDIR ${AIRFLOW_HOME}

ENV AIRFLOW__CORE__LOAD_EXAMPLES False
ENV AIRFLOW__DATABASE__LOAD_DEFAULT_CONNECTIONS False

VOLUME ["/opt/airflow/dags"]
EXPOSE 8080
