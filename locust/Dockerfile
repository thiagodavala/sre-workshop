FROM python:3.9
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir locust
EXPOSE 8089
CMD ["locust", "-f", "locustfile.py", "--host", "http://localhost:8001","--users", "10", "--spawn-rate", "1", "--run-time", "99999m", "--headless"]