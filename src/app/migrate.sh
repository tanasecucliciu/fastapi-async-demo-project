export PYTHONPATH="$(dirname "$(pwd)"):${PYTHONPATH}"
alembic upgrade head
