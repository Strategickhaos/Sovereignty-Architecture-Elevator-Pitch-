#!/usr/bin/env python3
# Simple embedding server
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from sentence_transformers import SentenceTransformer
import uvicorn
import os

app = FastAPI()

print('Loading BGE model...')
cache_dir = os.getenv('MODEL_CACHE', '/cache')
model = SentenceTransformer('BAAI/bge-small-en-v1.5', cache_folder=cache_dir)
print('Model loaded successfully')

class EmbedRequest(BaseModel):
    texts: List[str]

@app.post('/embed')
async def embed_texts(request: EmbedRequest):
    embeddings = model.encode(request.texts, normalize_embeddings=True).tolist()
    return {'embeddings': embeddings}

@app.get('/health')
async def health():
    return {'status': 'healthy', 'model': 'bge-small-en-v1.5'}

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8081)