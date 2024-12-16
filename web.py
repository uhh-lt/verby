import asyncio
from fastapi import FastAPI
from dataclasses import dataclass
from contextlib import asynccontextmanager

import verby

@dataclass
class InputData:
    text: str

nlp = None  # This will hold the model
nlp_lock = asyncio.Lock()  # Lock to control model access

@asynccontextmanager
async def lifespan(app: FastAPI):
    global nlp
    nlp = verby.pipeline.build_pipeline("de")  # Load your model here
    print("Model loaded")
    yield
    print("Shutting down")

app = FastAPI(lifespan=lifespan)

@app.post("/segment")
async def predict(data: InputData):
    async with nlp_lock:  # Lock access to the model
        doc = nlp(data.text)
    phrases_indices = []
    for phrase in doc._.verbal_phrases:
        phrase_indices = []
        for span in phrase:
            phrase_indices.append((span.start_char, span.end_char))
        phrases_indices.append(phrase_indices)
    sentence_indices = []
    for sent in doc.sents:
        sentence_indices.append((sent.start_char, sent.end_char))
    return {"verbal_phrases": phrases_indices, "sentences": sentence_indices}
