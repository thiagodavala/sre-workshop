FROM python:3.9-alpine
ENV LOCUST_VERSION=2.5.0
WORKDIR /app
COPY . /app
RUN apk --no-cache add \
        build-base \
        libffi-dev \
        openssl-dev \
        python3-dev \
        && pip install --no-cache-dir locustio==$LOCUST_VERSION

EXPOSE 8089
CMD ["locust", "-f", "locustfile.py", "--host", "http://localhost:8001", "--users", "10", "--spawn-rate", "1", "--run-time", "99999m", "--headless"]
