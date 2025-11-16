"""
Refinory Database Layer
PostgreSQL with vector extensions for AI agent orchestration
"""

import asyncio
import json
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
import asyncpg
import structlog

from .orchestrator import ArchitectureRequest, RequestStatus

logger = structlog.get_logger()

class Database:
    """Database connection and operations manager"""
    
    def __init__(self, dsn: str):
        self.dsn = dsn
        self.pool: Optional[asyncpg.Pool] = None
        
    async def initialize(self):
        """Initialize database connection pool and schema"""
        logger.info("Initializing database connection")
        
        self.pool = await asyncpg.create_pool(
            self.dsn,
            min_size=5,
            max_size=20,
            command_timeout=60
        )
        
        await self._create_schema()
        logger.info("Database initialized successfully")
    
    async def close(self):
        """Close database connection pool"""
        if self.pool:
            await self.pool.close()
            logger.info("Database connection pool closed")
    
    async def health_check(self):
        """Check database connectivity"""
        if not self.pool:
            raise Exception("Database not initialized")
        
        async with self.pool.acquire() as conn:
            result = await conn.fetchval("SELECT 1")
            if result != 1:
                raise Exception("Database health check failed")
    
    async def _create_schema(self):
        """Create database schema if not exists"""
        schema_sql = """
        -- Enable pgvector extension for vector operations
        CREATE EXTENSION IF NOT EXISTS vector;
        
        -- Architecture requests table
        CREATE TABLE IF NOT EXISTS architecture_requests (
            request_id UUID PRIMARY KEY,
            project_name VARCHAR(255) NOT NULL,
            description TEXT NOT NULL,
            requirements JSONB DEFAULT '[]',
            experts_requested JSONB DEFAULT '[]',
            priority VARCHAR(50) DEFAULT 'normal',
            github_repo VARCHAR(255),
            status VARCHAR(50) DEFAULT 'pending',
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            experts_assigned JSONB DEFAULT '[]',
            progress JSONB DEFAULT '{}',
            artifacts_url VARCHAR(500),
            github_pr_url VARCHAR(500)
        );
        
        -- Expert tasks table
        CREATE TABLE IF NOT EXISTS expert_tasks (
            task_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            request_id UUID NOT NULL REFERENCES architecture_requests(request_id) ON DELETE CASCADE,
            expert_name VARCHAR(100) NOT NULL,
            task_type VARCHAR(100) NOT NULL,
            context JSONB NOT NULL,
            dependencies JSONB DEFAULT '[]',
            status VARCHAR(50) DEFAULT 'pending',
            result JSONB,
            artifacts JSONB DEFAULT '[]',
            started_at TIMESTAMP WITH TIME ZONE,
            completed_at TIMESTAMP WITH TIME ZONE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        
        -- Expert capabilities cache
        CREATE TABLE IF NOT EXISTS expert_capabilities (
            expert_name VARCHAR(100) PRIMARY KEY,
            capabilities JSONB NOT NULL,
            technologies JSONB NOT NULL,
            task_types JSONB NOT NULL,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        
        -- Architecture artifacts storage
        CREATE TABLE IF NOT EXISTS architecture_artifacts (
            artifact_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            request_id UUID NOT NULL REFERENCES architecture_requests(request_id) ON DELETE CASCADE,
            artifact_type VARCHAR(100) NOT NULL,
            filename VARCHAR(255) NOT NULL,
            content TEXT,
            metadata JSONB DEFAULT '{}',
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        
        -- Vector embeddings for semantic search
        CREATE TABLE IF NOT EXISTS architecture_embeddings (
            embedding_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            request_id UUID NOT NULL REFERENCES architecture_requests(request_id) ON DELETE CASCADE,
            content_type VARCHAR(100) NOT NULL,
            content TEXT NOT NULL,
            embedding vector(1536), -- OpenAI embedding dimension
            metadata JSONB DEFAULT '{}',
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        
        -- Request metrics and analytics
        CREATE TABLE IF NOT EXISTS request_metrics (
            metric_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            request_id UUID NOT NULL REFERENCES architecture_requests(request_id) ON DELETE CASCADE,
            metric_name VARCHAR(100) NOT NULL,
            metric_value FLOAT NOT NULL,
            dimensions JSONB DEFAULT '{}',
            timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        
        -- Indexes for performance
        CREATE INDEX IF NOT EXISTS idx_architecture_requests_status ON architecture_requests(status);
        CREATE INDEX IF NOT EXISTS idx_architecture_requests_created_at ON architecture_requests(created_at DESC);
        CREATE INDEX IF NOT EXISTS idx_expert_tasks_request_id ON expert_tasks(request_id);
        CREATE INDEX IF NOT EXISTS idx_expert_tasks_expert_status ON expert_tasks(expert_name, status);
        CREATE INDEX IF NOT EXISTS idx_architecture_artifacts_request_id ON architecture_artifacts(request_id);
        CREATE INDEX IF NOT EXISTS idx_architecture_embeddings_request_id ON architecture_embeddings(request_id);
        CREATE INDEX IF NOT EXISTS idx_request_metrics_request_id ON request_metrics(request_id);
        
        -- Updated at trigger function
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = NOW();
            RETURN NEW;
        END;
        $$ language 'plpgsql';
        
        -- Apply updated_at triggers
        DROP TRIGGER IF EXISTS update_architecture_requests_updated_at ON architecture_requests;
        CREATE TRIGGER update_architecture_requests_updated_at
            BEFORE UPDATE ON architecture_requests
            FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
        """
        
        async with self.pool.acquire() as conn:
            await conn.execute(schema_sql)
            logger.info("Database schema created/updated successfully")
    
    # Architecture Request operations
    async def store_architecture_request(self, request: ArchitectureRequest):
        """Store new architecture request"""
        sql = """
        INSERT INTO architecture_requests (
            request_id, project_name, description, requirements, experts_requested,
            priority, github_repo, status, created_at, experts_assigned, progress
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
        """
        
        async with self.pool.acquire() as conn:
            await conn.execute(
                sql,
                request.request_id,
                request.project_name,
                request.description,
                json.dumps(request.requirements),
                json.dumps(request.experts_requested) if request.experts_requested else json.dumps([]),
                request.priority,
                request.github_repo,
                request.status.value,
                request.created_at,
                json.dumps(request.experts_assigned) if request.experts_assigned else json.dumps([]),
                json.dumps(request.progress) if request.progress else json.dumps({})
            )
    
    async def get_architecture_request(self, request_id: str) -> ArchitectureRequest:
        """Get architecture request by ID"""
        sql = """
        SELECT request_id, project_name, description, requirements, experts_requested,
               priority, github_repo, status, created_at, experts_assigned, progress,
               artifacts_url, github_pr_url
        FROM architecture_requests 
        WHERE request_id = $1
        """
        
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(sql, request_id)
            
            if not row:
                raise ValueError(f"Request {request_id} not found")
            
            return ArchitectureRequest(
                request_id=str(row['request_id']),
                project_name=row['project_name'],
                description=row['description'],
                requirements=json.loads(row['requirements']) if row['requirements'] else [],
                experts_requested=json.loads(row['experts_requested']) if row['experts_requested'] else None,
                priority=row['priority'],
                github_repo=row['github_repo'],
                status=RequestStatus(row['status']),
                created_at=row['created_at'],
                experts_assigned=json.loads(row['experts_assigned']) if row['experts_assigned'] else [],
                progress=json.loads(row['progress']) if row['progress'] else {},
                artifacts_url=row['artifacts_url'],
                github_pr_url=row['github_pr_url']
            )
    
    async def update_architecture_request(self, request: ArchitectureRequest):
        """Update existing architecture request"""
        sql = """
        UPDATE architecture_requests SET
            project_name = $2,
            description = $3, 
            requirements = $4,
            experts_requested = $5,
            priority = $6,
            github_repo = $7,
            status = $8,
            experts_assigned = $9,
            progress = $10,
            artifacts_url = $11,
            github_pr_url = $12
        WHERE request_id = $1
        """
        
        async with self.pool.acquire() as conn:
            await conn.execute(
                sql,
                request.request_id,
                request.project_name,
                request.description,
                json.dumps(request.requirements),
                json.dumps(request.experts_requested) if request.experts_requested else None,
                request.priority,
                request.github_repo,
                request.status.value,
                json.dumps(request.experts_assigned),
                json.dumps(request.progress),
                request.artifacts_url,
                request.github_pr_url
            )
    
    async def list_architecture_requests(
        self, 
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[ArchitectureRequest]:
        """List architecture requests with optional filtering"""
        
        where_clause = "WHERE status = $1" if status else ""
        params = [status] if status else []
        
        sql = f"""
        SELECT request_id, project_name, description, requirements, experts_requested,
               priority, github_repo, status, created_at, experts_assigned, progress,
               artifacts_url, github_pr_url
        FROM architecture_requests
        {where_clause}
        ORDER BY created_at DESC
        LIMIT ${len(params) + 1} OFFSET ${len(params) + 2}
        """
        
        params.extend([limit, offset])
        
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(sql, *params)
            
            return [
                ArchitectureRequest(
                    request_id=str(row['request_id']),
                    project_name=row['project_name'],
                    description=row['description'],
                    requirements=json.loads(row['requirements']) if row['requirements'] else [],
                    experts_requested=json.loads(row['experts_requested']) if row['experts_requested'] else None,
                    priority=row['priority'],
                    github_repo=row['github_repo'],
                    status=RequestStatus(row['status']),
                    created_at=row['created_at'],
                    experts_assigned=json.loads(row['experts_assigned']) if row['experts_assigned'] else [],
                    progress=json.loads(row['progress']) if row['progress'] else {},
                    artifacts_url=row['artifacts_url'],
                    github_pr_url=row['github_pr_url']
                )
                for row in rows
            ]
    
    async def update_request_status(self, request_id: str, status: str, progress: Dict[str, Any]):
        """Update request status and progress"""
        sql = """
        UPDATE architecture_requests 
        SET status = $2, progress = $3
        WHERE request_id = $1
        """
        
        async with self.pool.acquire() as conn:
            await conn.execute(sql, request_id, status, json.dumps(progress))
    
    async def update_request_github_pr(self, request_id: str, pr_url: str):
        """Update GitHub PR URL for request"""
        sql = """
        UPDATE architecture_requests 
        SET github_pr_url = $2
        WHERE request_id = $1
        """
        
        async with self.pool.acquire() as conn:
            await conn.execute(sql, request_id, pr_url)
    
    # Expert task operations
    async def store_expert_task(self, task_data: Dict[str, Any]):
        """Store expert task"""
        sql = """
        INSERT INTO expert_tasks (
            request_id, expert_name, task_type, context, dependencies, status
        ) VALUES ($1, $2, $3, $4, $5, $6)
        RETURNING task_id
        """
        
        async with self.pool.acquire() as conn:
            task_id = await conn.fetchval(
                sql,
                task_data['request_id'],
                task_data['expert_name'],
                task_data['task_type'],
                json.dumps(task_data['context']),
                json.dumps(task_data.get('dependencies', [])),
                task_data.get('status', 'pending')
            )
            return str(task_id)
    
    async def update_expert_task_result(self, task_id: str, result: Dict[str, Any], status: str = 'completed'):
        """Update expert task with result"""
        sql = """
        UPDATE expert_tasks 
        SET result = $2, status = $3, completed_at = NOW()
        WHERE task_id = $1
        """
        
        async with self.pool.acquire() as conn:
            await conn.execute(sql, task_id, json.dumps(result), status)
    
    # Artifact operations
    async def store_architecture_artifact(
        self, 
        request_id: str, 
        artifact_type: str, 
        filename: str, 
        content: str,
        metadata: Dict[str, Any] = None
    ) -> str:
        """Store architecture artifact"""
        sql = """
        INSERT INTO architecture_artifacts (
            request_id, artifact_type, filename, content, metadata
        ) VALUES ($1, $2, $3, $4, $5)
        RETURNING artifact_id
        """
        
        async with self.pool.acquire() as conn:
            artifact_id = await conn.fetchval(
                sql,
                request_id,
                artifact_type,
                filename,
                content,
                json.dumps(metadata or {})
            )
            return str(artifact_id)
    
    async def get_request_artifacts(self, request_id: str) -> List[Dict[str, Any]]:
        """Get all artifacts for a request"""
        sql = """
        SELECT artifact_id, artifact_type, filename, content, metadata, created_at
        FROM architecture_artifacts
        WHERE request_id = $1
        ORDER BY created_at DESC
        """
        
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(sql, request_id)
            
            return [
                {
                    "artifact_id": str(row['artifact_id']),
                    "artifact_type": row['artifact_type'],
                    "filename": row['filename'],
                    "content": row['content'],
                    "metadata": json.loads(row['metadata']) if row['metadata'] else {},
                    "created_at": row['created_at']
                }
                for row in rows
            ]
    
    # Vector operations for semantic search
    async def store_embedding(
        self, 
        request_id: str, 
        content_type: str, 
        content: str, 
        embedding: List[float],
        metadata: Dict[str, Any] = None
    ) -> str:
        """Store content embedding for semantic search"""
        sql = """
        INSERT INTO architecture_embeddings (
            request_id, content_type, content, embedding, metadata
        ) VALUES ($1, $2, $3, $4, $5)
        RETURNING embedding_id
        """
        
        async with self.pool.acquire() as conn:
            embedding_id = await conn.fetchval(
                sql,
                request_id,
                content_type,
                content,
                embedding,  # pgvector will handle the conversion
                json.dumps(metadata or {})
            )
            return str(embedding_id)
    
    async def semantic_search(
        self, 
        query_embedding: List[float], 
        content_type: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Perform semantic search using vector similarity"""
        where_clause = "WHERE content_type = $2" if content_type else ""
        params = [query_embedding]
        if content_type:
            params.append(content_type)
        
        sql = f"""
        SELECT e.request_id, e.content_type, e.content, e.metadata,
               r.project_name, r.description,
               (e.embedding <-> $1) as distance
        FROM architecture_embeddings e
        JOIN architecture_requests r ON e.request_id = r.request_id
        {where_clause}
        ORDER BY e.embedding <-> $1
        LIMIT ${len(params) + 1}
        """
        
        params.append(limit)
        
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(sql, *params)
            
            return [
                {
                    "request_id": str(row['request_id']),
                    "content_type": row['content_type'],
                    "content": row['content'],
                    "metadata": json.loads(row['metadata']) if row['metadata'] else {},
                    "project_name": row['project_name'],
                    "description": row['description'],
                    "similarity_score": 1.0 - float(row['distance'])  # Convert distance to similarity
                }
                for row in rows
            ]
    
    # Metrics operations
    async def record_metric(
        self, 
        request_id: str, 
        metric_name: str, 
        metric_value: float,
        dimensions: Dict[str, Any] = None
    ):
        """Record performance metric"""
        sql = """
        INSERT INTO request_metrics (request_id, metric_name, metric_value, dimensions)
        VALUES ($1, $2, $3, $4)
        """
        
        async with self.pool.acquire() as conn:
            await conn.execute(
                sql,
                request_id,
                metric_name,
                metric_value,
                json.dumps(dimensions or {})
            )
    
    async def get_request_metrics(
        self, 
        request_id: str, 
        metric_name: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get metrics for a request"""
        where_clause = "WHERE request_id = $1"
        params = [request_id]
        
        if metric_name:
            where_clause += " AND metric_name = $2"
            params.append(metric_name)
        
        sql = f"""
        SELECT metric_name, metric_value, dimensions, timestamp
        FROM request_metrics
        {where_clause}
        ORDER BY timestamp DESC
        """
        
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(sql, *params)
            
            return [
                {
                    "metric_name": row['metric_name'],
                    "metric_value": float(row['metric_value']),
                    "dimensions": json.loads(row['dimensions']) if row['dimensions'] else {},
                    "timestamp": row['timestamp']
                }
                for row in rows
            ]

# Dependency injection helper
def get_db() -> Database:
    """Get database instance (to be used with dependency injection)"""
    # This will be set up properly in the main application
    pass