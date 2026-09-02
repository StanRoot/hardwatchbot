FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir --requirement requirements.txt

RUN addgroup --system bot \
    && adduser --system --ingroup bot bot

COPY --chown=bot:bot app ./

USER bot

CMD ["python", "test.py"]
