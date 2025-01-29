FROM python:3.11-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:0.5.25 /uv /uvx /bin/

RUN apt-get update
RUN apt-get install -y --no-install-recommends make build-essential libsnappy1v5 libsnappy-dev 

# Copy the project into the image
ADD . /app

# Sync the project into a new environment, using the frozen lockfile
WORKDIR /app
RUN uv sync --frozen

EXPOSE 80
CMD ["uv", "run", "gunicorn", "--conf", "gunicorn_conf.py", "--bind", "0.0.0.0:80", "wsgi:app"]
