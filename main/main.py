from fastapi import FastAPI, HTTPException
import httpx
import random
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
import os

SIGNOZ_URL = os.getenv("SIGNOZ_URL", "http://localhost:4317")

resource = Resource(attributes={"service.name": "petshop"})
provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)

otlp_exporter = OTLPSpanExporter(endpoint=SIGNOZ_URL, insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
provider.add_span_processor(span_processor)

app = FastAPI()

FastAPIInstrumentor.instrument_app(app)
HTTPXClientInstrumentor().instrument()

@app.get("/")
async def read_root():
    return {"message": "Petshop!"}

@app.get("/pets/get")
async def get_random_pet():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("http://localhost:8001/pets/random")
            response.raise_for_status()
            pokemon = response.json()
            return pokemon
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail="Error fetching random pet")
        except Exception as e:
            raise HTTPException(status_code=500, detail="Internal server error")
        

