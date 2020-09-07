FROM python:3.8.2-slim as base

# Add build deps for python packages
# libpq-dev is required to install psycopg2-binary
# curl to install vendored poetry
RUN apt-get update && \
    apt-get install git curl libpq-dev gcc -y && \
    apt-get clean

# Set the working directory
WORKDIR /app

# Enable storing logs to S3
ENV S3_STORAGE_BACKEND=1
# Unbuffer python so that we ensure we get all of the logs
ENV PYTHONUNBUFFERED=1
# Set the poetry version
ENV POETRY_VERSION=1.0.5
# Add the poetry folder to the PATH
ENV PATH="/root/.poetry/bin:$PATH"


# Install vendored poetry
# Also set the virtualenv creation to false so we end up with 1 python installation instead of 2
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python && \
    poetry config virtualenvs.create false

# Add poetry stuff
ADD pyproject.toml .
ADD poetry.lock .

ARG install_dev
RUN poetry run pip install -U pip
RUN if [ "$install_dev" = "true" ] ; then poetry install ; else poetry install --ansi --no-dev ; fi && \
    rm -rf ~/.cache

# Add everything
ADD . .


