FROM python:3.10

WORKDIR /app/

COPY src/app /app

RUN python3 -m pip install -r requirements/base.txt

ENV PYTHONPATH=/:/app

COPY dist/app/scripts/start.sh /start.sh
RUN chmod +x /start.sh
