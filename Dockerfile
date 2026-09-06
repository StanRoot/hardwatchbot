FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        bash \
        procps \
        iproute2 \
        iputils-ping \
        curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/hardwatchbot

COPY requirements.txt ./
RUN pip install --no-cache-dir --requirement requirements.txt

RUN addgroup --system --gid 10001 bot \
    && adduser --system \
        --uid 10001 \
        --gid 10001 \
        --no-create-home \
        --disabled-login \
        bot

COPY --chown=bot:bot app ./app

USER bot

CMD ["python", "-m", "app.bot"]
