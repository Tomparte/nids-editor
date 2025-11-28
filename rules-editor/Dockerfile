FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir flask

COPY app.py .
COPY index.html .

ENV FLASK_APP=app.py
ENV RULES_FILE=/rules/local.rules

CMD ["python", "app.py"]
