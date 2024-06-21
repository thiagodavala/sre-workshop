from fastapi import FastAPI, HTTPException
import httpx
import random
import asyncio
from pydantic import BaseModel
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
import os

SIGNOZ_URL = os.getenv("SIGNOZ_URL", "http://localhost:4317")

resource = Resource(attributes={"service.name": "pets"})
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
    return {"message": "Au! Au!"}

async def zipcode_check():
    async with httpx.AsyncClient() as client:
        try:
            await asyncio.sleep(40)
            response = await client.get(f"https://viacep.com.br/ws/80410201/json/")
            response.raise_for_status()
            data = response.json()
            if "erro" in data:
                raise HTTPException(status_code=404, detail="Zip code not found")
            return "Checkout successful"
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail="Error fetching zip code")
        except Exception as e:
            raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/pets/checkout")
async def checkout():
    result = await zipcode_check()
    return {"message": result}

# Lista de produtos de pet shop
pet_products = [
    "Dog Toy",
    "Cat Food",
    "Bird Cage",
    "Fish Tank",
    "Hamster Wheel"
]

@app.get("/pets/products/{id}")
async def get_pet_product(id: int):
    if id == 10101:
        raise HTTPException(status_code=500, detail="Internal server error")
    product = random.choice(pet_products)
    return {"product": product}

# Métodos de verificação de estoque
async def physical_store(product_id: int):
    # Simula a verificação de estoque na loja física
    await asyncio.sleep(random.uniform(0.1, 0.5))  # Simula latência
    return {"physical_store": random.choice([True, False])}

async def third_party_stock(product_id: int):
    # Simula a verificação de estoque em terceiros
    await asyncio.sleep(random.uniform(0.1, 0.5))  # Simula latência
    return {"third_party_stock": random.choice([True, False])}

async def central_warehouse(product_id: int):
    # Simula a verificação de estoque no armazém central
    await asyncio.sleep(random.uniform(0.1, 0.5))  # Simula latência
    raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/pets/check_stock/{product_id}")
async def check_stock(product_id: int):
    try:
        # Executa as três verificações de estoque em paralelo
        results = await asyncio.gather(
            physical_store(product_id),
            third_party_stock(product_id),
            central_warehouse(product_id)
        )
        
        # Agrega os resultados em um único dicionário
        stock_status = {k: v for d in results for k, v in d.items()}
        
        return stock_status
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    
class LoginData(BaseModel):
    login: str
    password: str

@app.post("/login")
async def login(data: LoginData):
    # Aqui você pode adicionar lógica de autenticação, como verificar o login e senha em um banco de dados.
    if data.login == "admin" and data.password == "secret":
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid login or password")

