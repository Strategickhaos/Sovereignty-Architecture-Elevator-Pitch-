"""
SAGCO API - FastAPI REST API
Provides HTTP endpoints for SAGCO kernel management
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import asyncio
import logging

from src.core import SAGCOKernel, Task, ProcessingNode, LayerType, create_sagco_kernel

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="SAGCO OS API",
    description="Sovereignty Architecture Governance Cognitive OS - REST API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global kernel instance
kernel: Optional[SAGCOKernel] = None


# ===== Models =====

class TaskSubmission(BaseModel):
    """Model for submitting a task"""
    task_id: str
    task_type: str
    payload: Dict[str, Any]
    priority: int = 0


class NodeRegistration(BaseModel):
    """Model for registering a node"""
    node_id: str
    layer: str
    capacity: int = 100


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    kernel_running: bool


class StatsResponse(BaseModel):
    """Statistics response"""
    total_nodes: int
    total_tasks: int
    completed_tasks: int
    failed_tasks: int
    pending_tasks: int
    running_tasks: int
    average_reward: float
    queue_length: int


# ===== Lifecycle Events =====

@app.on_event("startup")
async def startup_event():
    """Initialize kernel on startup"""
    global kernel
    logger.info("Starting SAGCO API...")
    
    try:
        # Create kernel with config
        kernel = create_sagco_kernel("/app/config/sagco.yaml")
        
        # Register default nodes
        for layer in LayerType:
            for i in range(2):
                node = ProcessingNode(
                    node_id=f"{layer.value}-node-{i}",
                    layer=layer,
                    capacity=10
                )
                kernel.register_node(node)
        
        # Start kernel
        await kernel.start()
        logger.info("SAGCO kernel started successfully")
        
    except Exception as e:
        logger.error(f"Failed to start kernel: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Stop kernel on shutdown"""
    global kernel
    logger.info("Shutting down SAGCO API...")
    
    if kernel:
        await kernel.stop()
        logger.info("SAGCO kernel stopped")


# ===== Health Endpoints =====

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy" if kernel and kernel.running else "unhealthy",
        "version": "0.1.0",
        "kernel_running": kernel.running if kernel else False
    }


@app.get("/ready", tags=["Health"])
async def readiness_check():
    """Readiness check endpoint"""
    if not kernel or not kernel.running:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Kernel not ready"
        )
    return {"status": "ready"}


# ===== Statistics Endpoints =====

@app.get("/stats", response_model=StatsResponse, tags=["Statistics"])
async def get_statistics():
    """Get kernel statistics"""
    if not kernel:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Kernel not available"
        )
    
    return kernel.get_statistics()


@app.get("/health-status", tags=["Statistics"])
async def get_health_status():
    """Get system health status"""
    if not kernel:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Kernel not available"
        )
    
    return kernel.get_health_status()


# ===== Task Management =====

@app.post("/tasks", tags=["Tasks"])
async def submit_task(task: TaskSubmission):
    """Submit a task for processing"""
    if not kernel:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Kernel not available"
        )
    
    try:
        task_obj = Task(
            task_id=task.task_id,
            task_type=task.task_type,
            payload=task.payload,
            priority=task.priority
        )
        task_id = kernel.submit_task(task_obj)
        return {"task_id": task_id, "status": "submitted"}
    
    except Exception as e:
        logger.error(f"Failed to submit task: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.get("/tasks/{task_id}", tags=["Tasks"])
async def get_task(task_id: str):
    """Get task details"""
    if not kernel:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Kernel not available"
        )
    
    if task_id not in kernel.tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    task = kernel.tasks[task_id]
    return {
        "task_id": task.task_id,
        "task_type": task.task_type,
        "status": task.status,
        "priority": task.priority,
        "result": task.result,
        "dopamine_reward": task.dopamine_reward,
        "created_at": task.created_at.isoformat() if task.created_at else None
    }


@app.get("/tasks", tags=["Tasks"])
async def list_tasks(status_filter: Optional[str] = None):
    """List all tasks with optional status filter"""
    if not kernel:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Kernel not available"
        )
    
    tasks = kernel.tasks.values()
    
    if status_filter:
        tasks = [t for t in tasks if t.status == status_filter]
    
    return {
        "tasks": [
            {
                "task_id": t.task_id,
                "task_type": t.task_type,
                "status": t.status,
                "priority": t.priority,
                "dopamine_reward": t.dopamine_reward
            }
            for t in tasks
        ],
        "count": len(list(tasks))
    }


# ===== Node Management =====

@app.post("/nodes", tags=["Nodes"])
async def register_node(node: NodeRegistration):
    """Register a new processing node"""
    if not kernel:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Kernel not available"
        )
    
    try:
        layer = LayerType(node.layer)
        node_obj = ProcessingNode(
            node_id=node.node_id,
            layer=layer,
            capacity=node.capacity
        )
        kernel.register_node(node_obj)
        return {"node_id": node.node_id, "status": "registered"}
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid layer: {node.layer}"
        )
    except Exception as e:
        logger.error(f"Failed to register node: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.get("/nodes", tags=["Nodes"])
async def list_nodes():
    """List all registered nodes"""
    if not kernel:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Kernel not available"
        )
    
    return {
        "nodes": [
            {
                "node_id": n.node_id,
                "layer": n.layer.value,
                "capacity": n.capacity,
                "current_load": n.current_load,
                "health_score": n.health_score,
                "utilization": n.get_utilization(),
                "available": n.is_available()
            }
            for n in kernel.nodes.values()
        ],
        "count": len(kernel.nodes)
    }


@app.delete("/nodes/{node_id}", tags=["Nodes"])
async def unregister_node(node_id: str):
    """Unregister a node"""
    if not kernel:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Kernel not available"
        )
    
    if node_id not in kernel.nodes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Node not found"
        )
    
    kernel.unregister_node(node_id)
    return {"node_id": node_id, "status": "unregistered"}


# ===== Root Endpoint =====

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "name": "SAGCO OS API",
        "version": "0.1.0",
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }


# For running with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
