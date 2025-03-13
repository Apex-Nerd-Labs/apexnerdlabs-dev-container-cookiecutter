#! /usr/bin/env bash

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env

cd boxtalk_data_sync

# Install Dependencies
uv sync --extra dev

# Install pre-commit hooks
uv run pre-commit install --install-hooks

cd /workspaces/.devcontainer
# Check if postgres is running
if [ -z "$(docker compose -f docker-compose.yml ps | grep 'postgres')" ]; then
    echo "Postgres is not running, starting it..."
    docker compose -f docker-compose.yml up -d --remove-orphans
fi

cd /workspaces/boxtalk_data_sync
# Run migrations
uv run alembic upgrade head

# Run tests
uv run pytest
