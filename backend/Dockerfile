###############################################
# Python FastAPI Runtime (Migrated Backend)   #
# Goal: minimal production image size         #
###############################################

FROM python:3.12-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
		PYTHONUNBUFFERED=1 \
		PIP_NO_CACHE_DIR=off \
		PIP_DISABLE_PIP_VERSION_CHECK=on \
		PIP_DEFAULT_TIMEOUT=100 \
		APP_HOME=/app \
		PORT=8000 \
		HOST=0.0.0.0

WORKDIR $APP_HOME

RUN apt-get update && apt-get install -y --no-install-recommends \
		build-essential gcc wget && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock* ./

RUN pip install --upgrade pip && pip install fastapi[standard] uvicorn[standard] asyncpg sqlalchemy alembic python-dotenv bcrypt authlib websockets

COPY main.py ./
COPY config ./config
COPY models ./models
COPY utils ./utils
## Optional folders (copy only if exist)
RUN [ -d py_routes ] && cp -r py_routes ./py_routes || true
RUN [ -d security ] && cp -r security ./security || true
RUN [ -d services ] && cp -r services ./services || true

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
	CMD python -c "import urllib.request,os;urllib.request.urlopen(f'http://127.0.0.1:{os.environ.get('PORT','8000')}/health')" || exit 1

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

