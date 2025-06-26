FROM ghcr.io/astral-sh/uv:debian-slim

WORKDIR /root

COPY pyproject.toml /root/
COPY uv.lock /root/

COPY src /root/src

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--workers", "1", "--log-level", "info"]