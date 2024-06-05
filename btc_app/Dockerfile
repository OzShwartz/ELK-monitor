FROM python:3.9-slim

WORKDIR /app

COPY btc_metric.py /app

RUN pip install prometheus_client requests

EXPOSE 8000

CMD ["python", "btc_metric.py"]
