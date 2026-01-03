FROM python:3.14-slim AS base

ENV PYTHONDONTWRITE_BYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	APP_HOME=/app \
	UV_SYSTEM_PYTHON=1 \
	PORT=8000 \
	HOST=0.0.0.0

WORKDIR ${APP_HOME}

# system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
	build-essential gcc curl \
	&& rm -rf /var/lib/apt/lists/*

# install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
	&& ln -s /root/.local/bin/uv /usr/local/bin/uv

# deps first (cache-friendly)
COPY pyproject.toml uv.lock* ./

RUN uv pip install -r pyproject.toml --system

# app source
COPY main.py alembic.ini ./
COPY config ./config
COPY middleware ./middleware
COPY migrations ./migrations
COPY models ./models
COPY repositories ./repositories
COPY routes ./routes
COPY schemas ./schemas
COPY services ./services
COPY templates ./templates
COPY utils ./utils

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
	CMD python - <<EOF || exit 1 import os, urllib.request urllib.request.urlopen(f"http://127.0.0.1:{os.getenv('PORT', '8000')}/health") EOF

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
