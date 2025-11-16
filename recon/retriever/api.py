#!/usr/bin/env python3
# RECON Retriever - RAG API for Strategic Khaos
# Fast semantic search and LLM-augmented responses

import os
import time
import asyncio
from typing import List, Dict, Optional
from datetime import datetime

import httpx
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from fastapi.responses import Response

# Configuration
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION = os.getenv("COLLECTION", "sovereignty-arch")
LLM_URL = os.getenv("LLM_URL", "http://localhost:8080")
EMBED_URL = os.getenv("EMBED_URL", "http://localhost:8081/embed")
MAX_CONTEXT_LENGTH = int(os.getenv("MAX_CONTEXT_LENGTH", "4000"))
RELEVANCE_THRESHOLD = float(os.getenv("RELEVANCE_THRESHOLD", "0.7"))

# Metrics
QUERY_COUNTER = Counter('rag_queries_total', 'Total RAG queries', ['collection', 'status'])
QUERY_DURATION = Histogram('rag_query_duration_seconds', 'Query processing time', ['operation'])
CONTEXT_RELEVANCE = Gauge('rag_context_relevance_score', 'Average context relevance score')
EMBEDDING_CACHE_HITS = Counter('rag_embedding_cache_hits_total', 'Embedding cache hits')

# Initialize FastAPI
app = FastAPI(
    title="RECON RAG API",
    description="Strategic Khaos Repository Analysis via RAG",
    version="2.0.0"
)

# CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global clients
qdrant_client = QdrantClient(url=QDRANT_URL)
httpx_client = None
embedding_cache = {}  # Simple in-memory cache

# Request/Response Models
class QueryRequest(BaseModel):
    q: str = Field(..., description="Query text")
    k: int = Field(default=8, ge=1, le=20, description="Number of results")
    collection: str = Field(default=COLLECTION, description="Collection name")
    path_prefix: Optional[str] = Field(default=None, description="Filter by path prefix")
    min_score: Optional[float] = Field(default=0.7, description="Minimum relevance score")
    include_llm: bool = Field(default=True, description="Include LLM response")

class ContextResult(BaseModel):
    path: str
    chunk: int
    score: float
    text: str
    metadata: Dict

class QueryResponse(BaseModel):
    query: str
    answer: Optional[str] = None
    contexts: List[ContextResult]
    total_contexts: int
    processing_time: float
    timestamp: datetime
    collection: str

class HealthResponse(BaseModel):
    status: str
    qdrant_status: str
    embedder_status: str
    llm_status: str
    collection_info: Dict
    uptime: float

# Startup/Shutdown
start_time = time.time()

@app.on_event("startup")
async def startup_event():
    global httpx_client
    httpx_client = httpx.AsyncClient(timeout=120)
    print("🚀 RECON RAG API started")
    print(f"   Qdrant: {QDRANT_URL}")
    print(f"   Collection: {COLLECTION}")
    print(f"   LLM: {LLM_URL}")
    print(f"   Embedder: {EMBED_URL}")

@app.on_event("shutdown")
async def shutdown_event():
    global httpx_client
    if httpx_client:
        await httpx_client.aclose()
    print("👋 RECON RAG API shutdown")

# Helper Functions
async def get_embedding(text: str) -> List[float]:
    """Get embedding for text with caching."""
    cache_key = hash(text)
    
    if cache_key in embedding_cache:
        EMBEDDING_CACHE_HITS.inc()
        return embedding_cache[cache_key]
    
    try:
        response = await httpx_client.post(
            EMBED_URL,
            json={"texts": [text]},
            timeout=30
        )
        response.raise_for_status()
        
        embeddings = response.json()["embeddings"]
        embedding = embeddings[0]
        
        # Cache with size limit
        if len(embedding_cache) < 1000:
            embedding_cache[cache_key] = embedding
        
        return embedding
        
    except Exception as e:
        print(f"❌ Embedding error: {e}")
        raise HTTPException(status_code=500, detail=f"Embedding service error: {e}")

async def search_contexts(query_vector: List[float], collection: str, k: int, 
                         path_prefix: Optional[str] = None, min_score: float = 0.7) -> List[ContextResult]:
    """Search for relevant contexts in Qdrant."""
    try:
        # Build query filter
        query_filter = None
        if path_prefix:
            query_filter = {
                "must": [
                    {
                        "key": "path",
                        "match": {
                            "value": path_prefix
                        }
                    }
                ]
            }
        
        # Search Qdrant
        search_result = qdrant_client.search(
            collection_name=collection,
            query_vector=query_vector,
            limit=k * 2,  # Get extra results for filtering
            query_filter=query_filter,
            with_payload=True,
            score_threshold=min_score
        )
        
        # Convert to ContextResult objects
        contexts = []
        for hit in search_result[:k]:  # Take top k after filtering
            contexts.append(ContextResult(
                path=hit.payload.get("path", "unknown"),
                chunk=hit.payload.get("chunk", 0),
                score=hit.score,
                text=hit.payload.get("text", ""),
                metadata={
                    "extension": hit.payload.get("extension", ""),
                    "file_size": hit.payload.get("file_size", 0),
                    "total_chunks": hit.payload.get("total_chunks", 1)
                }
            ))
        
        return contexts
        
    except Exception as e:
        print(f"❌ Search error: {e}")
        raise HTTPException(status_code=500, detail=f"Search error: {e}")

async def generate_llm_response(query: str, contexts: List[ContextResult]) -> Optional[str]:
    """Generate LLM response using retrieved contexts."""
    if not contexts:
        return None
    
    # Build context string with source attribution
    context_parts = []
    total_length = 0
    
    for ctx in contexts:
        context_part = f"// Source: {ctx.path} (chunk {ctx.chunk}, score: {ctx.score:.3f})\n{ctx.text}"
        
        if total_length + len(context_part) > MAX_CONTEXT_LENGTH:
            break
            
        context_parts.append(context_part)
        total_length += len(context_part)
    
    context_text = "\n\n".join(context_parts)
    
    # Construct prompt
    prompt = f"""You are an expert software architect analyzing the Strategic Khaos sovereignty architecture.

Use ONLY the provided code context to answer questions accurately and comprehensively.
If the context doesn't contain relevant information, say so clearly.

Context:
{context_text}

Question: {query}

Provide a detailed, technical answer based on the code context above:"""
    
    try:
        # Call LLM
        response = await httpx_client.post(
            f"{LLM_URL}/completion",
            json={
                "prompt": prompt,
                "n_predict": 512,
                "temperature": 0.1,
                "stop": ["Human:", "Question:"],
                "repeat_penalty": 1.1
            },
            timeout=90
        )
        
        if response.status_code != 200:
            print(f"⚠️ LLM returned status {response.status_code}")
            return None
        
        result = response.json()
        answer = result.get("content", "").strip()
        
        return answer if answer else None
        
    except Exception as e:
        print(f"❌ LLM generation error: {e}")
        return None

# API Endpoints
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    
    # Check Qdrant
    qdrant_status = "unknown"
    collection_info = {}
    try:
        collections = qdrant_client.get_collections()
        qdrant_status = "healthy"
        
        # Get collection info if it exists
        if any(c.name == COLLECTION for c in collections.collections):
            info = qdrant_client.get_collection(COLLECTION)
            collection_info = {
                "vectors_count": info.vectors_count,
                "status": info.status
            }
    except Exception:
        qdrant_status = "unhealthy"
    
    # Check embedder
    embedder_status = "unknown"
    try:
        response = await httpx_client.get(f"{EMBED_URL.replace('/embed', '')}/health", timeout=5)
        embedder_status = "healthy" if response.status_code == 200 else "unhealthy"
    except Exception:
        embedder_status = "unhealthy"
    
    # Check LLM
    llm_status = "unknown"
    try:
        response = await httpx_client.get(f"{LLM_URL}/health", timeout=5)
        llm_status = "healthy" if response.status_code == 200 else "unhealthy"
    except Exception:
        llm_status = "unhealthy"
    
    overall_status = "healthy" if all([
        qdrant_status == "healthy",
        embedder_status == "healthy"
    ]) else "degraded"
    
    return HealthResponse(
        status=overall_status,
        qdrant_status=qdrant_status,
        embedder_status=embedder_status,
        llm_status=llm_status,
        collection_info=collection_info,
        uptime=time.time() - start_time
    )

@app.post("/query", response_model=QueryResponse)
async def query_repository(request: QueryRequest, background_tasks: BackgroundTasks):
    """Main RAG query endpoint."""
    start_time = time.time()
    
    with QUERY_DURATION.labels(operation="total").time():
        try:
            # Get query embedding
            with QUERY_DURATION.labels(operation="embedding").time():
                query_vector = await get_embedding(request.q)
            
            # Search for contexts
            with QUERY_DURATION.labels(operation="search").time():
                contexts = await search_contexts(
                    query_vector=query_vector,
                    collection=request.collection,
                    k=request.k,
                    path_prefix=request.path_prefix,
                    min_score=request.min_score
                )
            
            # Calculate average relevance
            if contexts:
                avg_relevance = sum(ctx.score for ctx in contexts) / len(contexts)
                CONTEXT_RELEVANCE.set(avg_relevance)
            
            # Generate LLM response if requested
            answer = None
            if request.include_llm and contexts:
                with QUERY_DURATION.labels(operation="llm").time():
                    answer = await generate_llm_response(request.q, contexts)
            
            processing_time = time.time() - start_time
            
            # Log successful query
            QUERY_COUNTER.labels(collection=request.collection, status="success").inc()
            
            return QueryResponse(
                query=request.q,
                answer=answer,
                contexts=contexts,
                total_contexts=len(contexts),
                processing_time=processing_time,
                timestamp=datetime.now(),
                collection=request.collection
            )
            
        except Exception as e:
            QUERY_COUNTER.labels(collection=request.collection, status="error").inc()
            print(f"❌ Query error: {e}")
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/collections")
async def list_collections():
    """List available collections."""
    try:
        collections = qdrant_client.get_collections()
        return {
            "collections": [
                {
                    "name": c.name,
                    "vectors_count": qdrant_client.get_collection(c.name).vectors_count
                }
                for c in collections.collections
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    return Response(generate_latest(), media_type="text/plain")

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "service": "RECON RAG API",
        "version": "2.0.0",
        "description": "Strategic Khaos Repository Analysis via RAG",
        "endpoints": {
            "query": "/query",
            "health": "/health",
            "collections": "/collections",
            "metrics": "/metrics"
        },
        "documentation": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7000)