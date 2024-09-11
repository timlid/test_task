FROM python:3.11.7

WORKDIR /app

RUN python -m venv .venv

ENV PATH="/app/.venv/bin:$PATH"

COPY . .

RUN apt-get update && apt-get install -y wget postgresql-client

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -U --no-cache-dir \
    --progress-bar off \
    --disable-pip-version-check \
    -r requirements.txt

RUN wget -O /usr/local/share/ca-certificates/global-bundle.pem https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem && \
    update-ca-certificates

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]