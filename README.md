# SRE Workshop

## Petshop System

### Apps

- petshop (main)
- pets
- customers

All applications implement Open Telemetry and are configured to send information locally to Signoz.io

## Test with Locust

```
docker run -p 8089:8089 -v $PWD/locust:/mnt/locust locustio/locust -f /mnt/locust/locustfile.py --host http://localhost:8000 --autostart
```
