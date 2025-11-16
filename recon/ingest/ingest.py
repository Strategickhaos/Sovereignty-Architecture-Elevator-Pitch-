#!/usr/bin/env python3
# RECON Ingest - Repository Indexer for RAG
# Optimized for Strategic Khaos sovereignty architecture

import os
import pathlib
import hashlib
import json
import asyncio
from typing import List, Dict, Optional, Tuple
import httpx
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct

# Configuration
RELEVANT_EXTENSIONS = {
    ".py", ".ts", ".tsx", ".js", ".java", ".go", ".rs", ".cs", 
    ".cpp", ".h", ".hpp", ".c", ".md", ".yaml", ".yml", 
    ".toml", ".json", ".txt", ".sh", ".ps1", ".dockerfile"
}

CHUNK_TOKENS = int(os.getenv("CHUNK_SIZE", "400"))
OVERLAP_TOKENS = int(os.getenv("OVERLAP", "60"))
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "32"))
MAX_FILE_SIZE = 2_000_000  # 2MB limit

IGNORE_DIRECTORIES = {
    "node_modules", "dist", ".git", "__pycache__", ".venv", 
    "venv", "build", "target", ".next", ".nuxt", "coverage",
    ".pytest_cache", ".mypy_cache", "*.egg-info"
}

class RepositoryIngestor:
    def __init__(self, qdrant_url: str, embed_url: str, collection: str):
        self.qdrant_client = QdrantClient(url=qdrant_url)
        self.embed_url = embed_url
        self.collection = collection
        self.session = None
        
    async def __aenter__(self):
        self.session = httpx.AsyncClient(timeout=120)
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.aclose()
    
    def read_file_safe(self, file_path: pathlib.Path) -> Optional[str]:
        """Safely read file content with size and encoding checks."""
        try:
            if file_path.stat().st_size > MAX_FILE_SIZE:
                print(f"⚠️  Skipping large file: {file_path} ({file_path.stat().st_size} bytes)")
                return None
                
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                
            # Skip empty or very short files
            if len(content.strip()) < 10:
                return None
                
            return content
            
        except Exception as e:
            print(f"❌ Error reading {file_path}: {e}")
            return None
    
    def chunk_text(self, text: str, chunk_size: int = CHUNK_TOKENS, overlap: int = OVERLAP_TOKENS) -> List[str]:
        """Split text into overlapping chunks based on word count."""
        words = text.split()
        
        if len(words) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(words):
            end = min(start + chunk_size, len(words))
            chunk = " ".join(words[start:end])
            chunks.append(chunk)
            
            # Move start position with overlap
            start = max(start + chunk_size - overlap, start + 1)
            
            if end == len(words):
                break
                
        return chunks
    
    async def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Get embeddings from the embedding service."""
        try:
            response = await self.session.post(
                self.embed_url,
                json={"texts": texts},
                timeout=60
            )
            response.raise_for_status()
            result = response.json()
            return result["embeddings"]
            
        except Exception as e:
            print(f"❌ Embedding error: {e}")
            raise
    
    def ensure_collection_exists(self):
        """Create collection if it doesn't exist."""
        try:
            collections = [c.name for c in self.qdrant_client.get_collections().collections]
            
            if self.collection not in collections:
                print(f"📦 Creating collection: {self.collection}")
                self.qdrant_client.create_collection(
                    collection_name=self.collection,
                    vectors_config=VectorParams(
                        size=384,  # BGE small embedding dimension
                        distance=Distance.COSINE
                    )
                )
            else:
                print(f"✅ Collection exists: {self.collection}")
                
        except Exception as e:
            print(f"❌ Collection setup error: {e}")
            raise
    
    def discover_files(self, repo_path: pathlib.Path) -> List[pathlib.Path]:
        """Discover all relevant files in the repository."""
        files = []
        
        for root, dirs, filenames in os.walk(repo_path):
            # Filter out ignored directories
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRECTORIES]
            
            for filename in filenames:
                file_path = pathlib.Path(root) / filename
                
                if file_path.suffix.lower() in RELEVANT_EXTENSIONS:
                    files.append(file_path)
        
        print(f"🔍 Discovered {len(files)} relevant files")
        return files
    
    async def process_file(self, file_path: pathlib.Path, repo_root: pathlib.Path) -> List[Tuple[str, str, Dict]]:
        """Process a single file into chunks with metadata."""
        content = self.read_file_safe(file_path)
        if not content:
            return []
        
        relative_path = file_path.relative_to(repo_root)
        chunks = self.chunk_text(content)
        
        points = []
        for chunk_idx, chunk_text in enumerate(chunks):
            # Generate unique ID for this chunk
            chunk_id = hashlib.sha256(
                f"{relative_path}:{chunk_idx}:{chunk_text[:100]}".encode()
            ).hexdigest()
            
            # Create metadata
            metadata = {
                "path": str(relative_path),
                "chunk": chunk_idx,
                "total_chunks": len(chunks),
                "extension": file_path.suffix.lower(),
                "file_size": len(content),
                "chunk_size": len(chunk_text),
                "text": chunk_text  # Include text in payload for retrieval
            }
            
            points.append((chunk_id, chunk_text, metadata))
        
        return points
    
    async def ingest_repository(self, repo_path: str):
        """Main ingestion process for a repository."""
        print(f"🚀 Starting ingestion of: {repo_path}")
        
        repo_root = pathlib.Path(repo_path)
        if not repo_root.exists():
            raise ValueError(f"Repository path does not exist: {repo_path}")
        
        # Setup
        self.ensure_collection_exists()
        
        # Discover files
        files = self.discover_files(repo_root)
        
        if not files:
            print("⚠️  No relevant files found")
            return
        
        # Process files in batches
        all_points = []
        
        print(f"📝 Processing {len(files)} files...")
        for i, file_path in enumerate(files):
            try:
                points = await self.process_file(file_path, repo_root)
                all_points.extend(points)
                
                if (i + 1) % 10 == 0:
                    print(f"   Processed {i + 1}/{len(files)} files...")
                    
            except Exception as e:
                print(f"❌ Error processing {file_path}: {e}")
                continue
        
        if not all_points:
            print("⚠️  No chunks generated")
            return
        
        print(f"📊 Generated {len(all_points)} chunks total")
        
        # Process embeddings and upload in batches
        await self.upload_chunks_batched(all_points)
        
        print(f"✅ Ingestion complete! Indexed {len(all_points)} chunks")
    
    async def upload_chunks_batched(self, all_points: List[Tuple[str, str, Dict]]):
        """Upload chunks to Qdrant in batches with embeddings."""
        for i in range(0, len(all_points), BATCH_SIZE):
            batch = all_points[i:i + BATCH_SIZE]
            
            # Extract texts for embedding
            texts = [chunk_text for _, chunk_text, _ in batch]
            
            try:
                # Get embeddings for this batch
                embeddings = await self.get_embeddings(texts)
                
                # Create Qdrant points
                qdrant_points = [
                    PointStruct(
                        id=chunk_id,
                        vector=embedding,
                        payload=metadata
                    )
                    for (chunk_id, _, metadata), embedding in zip(batch, embeddings)
                ]
                
                # Upload to Qdrant
                self.qdrant_client.upsert(
                    collection_name=self.collection,
                    points=qdrant_points
                )
                
                print(f"   Uploaded batch {i//BATCH_SIZE + 1}/{(len(all_points) + BATCH_SIZE - 1)//BATCH_SIZE}")
                
            except Exception as e:
                print(f"❌ Batch upload error: {e}")
                continue

async def main():
    """Main entry point."""
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python ingest.py <repository_path>")
        sys.exit(1)
    
    repo_path = sys.argv[1]
    
    # Environment configuration
    qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
    embed_url = os.getenv("EMBED_URL", "http://localhost:8081/embed")
    collection = os.getenv("COLLECTION", "sovereignty-arch")
    
    print(f"🎯 RECON Ingestion Configuration:")
    print(f"   Repository: {repo_path}")
    print(f"   Qdrant: {qdrant_url}")
    print(f"   Embeddings: {embed_url}")
    print(f"   Collection: {collection}")
    print(f"   Chunk size: {CHUNK_TOKENS} tokens")
    print(f"   Overlap: {OVERLAP_TOKENS} tokens")
    print(f"   Batch size: {BATCH_SIZE}")
    print()
    
    # Wait for services to be ready
    print("⏳ Waiting for services...")
    await asyncio.sleep(10)
    
    # Start ingestion
    async with RepositoryIngestor(qdrant_url, embed_url, collection) as ingestor:
        await ingestor.ingest_repository(repo_path)

if __name__ == "__main__":
    asyncio.run(main())