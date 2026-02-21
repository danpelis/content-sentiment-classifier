FROM astral/uv:python3.12-bookworm-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen
ENV PYTHONUNBUFFERED=1

RUN useradd app && mkdir -p /home/app/.cache && chown -R app:app /home/app/.cache

COPY app ./app

USER app

EXPOSE 7860

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]