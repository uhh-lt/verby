import asyncio
from fastapi import FastAPI
from dataclasses import dataclass

import verby

@dataclass
class InputData:
    text: str

app = FastAPI()
nlp = None  # This will hold the model
nlp_lock = asyncio.Lock()  # Lock to control model access


@app.on_event("startup")
async def load_model():
    global model
    model = verby.pipeline.build_pipeline("de")  # Load your model here


@app.post("/segment")
async def predict(data: InputData):
    async with nlp_lock:  # Lock access to the model
        result = model(data.text)
    return {"result": result}
