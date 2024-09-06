
default: run

run:
    poetry run python -m archivebot.main run

initdb *args:
    poetry run python -m archivebot.main initdb {{ args }}

setup:
    poetry install

lint:
    poetry run black --check archivebot
    poetry run isort --check-only archivebot
    poetry run flake8 archivebot
    poetry run mypy archivebot

format:
    poetry run autoflake         --remove-all-unused-imports         --recursive         --in-place archivebot
    poetry run black archivebot
    poetry run isort archivebot

test:
    poetry run pytest --cov=archivebot --cov-report=html

watch *args:
    watchexec --clear 'just {{ args }}'
