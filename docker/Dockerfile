FROM python:3.10

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs > r.sh && sh r.sh -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Copying this first will improve caching and re-runs.
COPY poetry.lock pyproject.toml /app/

WORKDIR /app

# Project initialization:
# Disable using virtualenvs. Docker is already isolated environment.
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root

COPY . /app

RUN poetry install

ENTRYPOINT ["nerd_assistant"]
