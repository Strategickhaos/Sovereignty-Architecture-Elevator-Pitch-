# Sovereignty Architecture API Documentation

**Version:** 2.0.0  
**Last Updated:** December 22, 2025

This document provides comprehensive API documentation for all services in the Sovereignty Architecture ecosystem.

## Table of Contents

1. [RECON RAG API](#recon-rag-api)
2. [Event Gateway API](#event-gateway-api)
3. [Refinory Orchestrator API](#refinory-orchestrator-api)
4. [Discord Bot Commands](#discord-bot-commands)

---

## RECON RAG API

**Base URL:** `http://localhost:7000`  
**Service:** Retrieval-Augmented Generation (RAG) API for Strategic Khaos repository analysis  
**Technology:** FastAPI + Python 3

### Overview

The RECON RAG API provides semantic search and LLM-augmented responses for analyzing the Strategic Khaos sovereignty architecture codebase. It uses Qdrant for vector storage, embeddings for semantic search, and optional LLM integration for generating contextual responses.

### Authentication

Currently, no authentication is required. In production, implement bearer token authentication.

### Configuration

Environment variables:
- `QDRANT_URL`: Qdrant vector database URL (default: `http://localhost:6333`)
- `COLLECTION`: Default collection name (default: `sovereignty-arch`)
- `LLM_URL`: LLM service URL (default: `http://localhost:8080`)
- `EMBED_URL`: Embedding service URL (default: `http://localhost:8081/embed`)
- `MAX_CONTEXT_LENGTH`: Maximum context length in tokens (default: `4000`)
- `RELEVANCE_THRESHOLD`: Minimum relevance score (default: `0.7`)

### Endpoints

#### GET /health

Health check endpoint for monitoring service status.

**Response:** `200 OK`

```json
{
  "status": "healthy",
  "qdrant_status": "healthy",
  "embedder_status": "healthy",
  "llm_status": "healthy",
  "collection_info": {
    "vectors_count": 1234,
    "status": "green"
  },
  "uptime": 3600.5
}
```

**Response Fields:**
- `status`: Overall service status (`healthy`, `degraded`)
- `qdrant_status`: Vector database status
- `embedder_status`: Embedding service status
- `llm_status`: LLM service status
- `collection_info`: Information about the vector collection
- `uptime`: Service uptime in seconds

---

#### POST /query

Main RAG query endpoint for semantic search with optional LLM response.

**Request Body:**

```json
{
  "q": "How does the event gateway handle GitHub webhooks?",
  "k": 8,
  "collection": "sovereignty-arch",
  "path_prefix": "src/",
  "min_score": 0.7,
  "include_llm": true
}
```

**Request Fields:**
- `q` (required): Query text
- `k` (optional): Number of results to return (1-20, default: 8)
- `collection` (optional): Collection name (default: from config)
- `path_prefix` (optional): Filter results by path prefix
- `min_score` (optional): Minimum relevance score (0-1, default: 0.7)
- `include_llm` (optional): Include LLM-generated answer (default: true)

**Response:** `200 OK`

```json
{
  "query": "How does the event gateway handle GitHub webhooks?",
  "answer": "The event gateway handles GitHub webhooks by...",
  "contexts": [
    {
      "path": "src/routes/github.ts",
      "chunk": 0,
      "score": 0.92,
      "text": "import type { Request, Response } from \"express\"...",
      "metadata": {
        "extension": "ts",
        "file_size": 2048,
        "total_chunks": 1
      }
    }
  ],
  "total_contexts": 5,
  "processing_time": 1.234,
  "timestamp": "2025-12-22T22:00:00Z",
  "collection": "sovereignty-arch"
}
```

**Response Fields:**
- `query`: Original query text
- `answer`: LLM-generated answer (if `include_llm` is true)
- `contexts`: Array of relevant code contexts
  - `path`: File path
  - `chunk`: Chunk number within file
  - `score`: Relevance score (0-1)
  - `text`: Code snippet
  - `metadata`: Additional file metadata
- `total_contexts`: Total number of contexts returned
- `processing_time`: Processing time in seconds
- `timestamp`: Response timestamp
- `collection`: Collection name used

**Error Responses:**

- `400 Bad Request`: Invalid request parameters
- `500 Internal Server Error`: Service error (embedding, search, or LLM)

---

#### GET /collections

List available vector collections.

**Response:** `200 OK`

```json
{
  "collections": [
    {
      "name": "sovereignty-arch",
      "vectors_count": 1234
    },
    {
      "name": "other-repo",
      "vectors_count": 567
    }
  ]
}
```

---

#### GET /metrics

Prometheus metrics endpoint.

**Response:** `200 OK` (Content-Type: `text/plain`)

```
# HELP rag_queries_total Total RAG queries
# TYPE rag_queries_total counter
rag_queries_total{collection="sovereignty-arch",status="success"} 42

# HELP rag_query_duration_seconds Query processing time
# TYPE rag_query_duration_seconds histogram
rag_query_duration_seconds_bucket{operation="total",le="0.5"} 10
...
```

---

#### GET /

Root endpoint with API information and available endpoints.

**Response:** `200 OK`

```json
{
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
```

---

## Event Gateway API

**Base URL:** `http://localhost:3001`  
**Service:** GitHub webhook event router to Discord  
**Technology:** Express + TypeScript + Discord.js

### Overview

The Event Gateway receives GitHub webhook events and routes them to appropriate Discord channels with formatted messages.

### Authentication

Webhook requests must include valid HMAC-SHA256 signature in the `X-Hub-Signature-256` header.

### Configuration

Environment variables:
- `DISCORD_TOKEN`: Discord bot token
- `PRS_CHANNEL_ID`: Discord channel ID for pull requests
- `DEPLOYMENTS_CHANNEL_ID`: Discord channel ID for deployments
- `ALERTS_CHANNEL_ID`: Discord channel ID for alerts
- `GITHUB_WEBHOOK_SECRET`: GitHub webhook secret for HMAC verification
- `PORT`: Server port (default: 3001)

### Endpoints

#### POST /webhooks/github

Receive and process GitHub webhook events.

**Headers:**
- `X-GitHub-Event`: GitHub event type (required)
- `X-Hub-Signature-256`: HMAC signature for verification (required)
- `Content-Type`: `application/json`

**Supported Events:**

##### pull_request

Handles pull request events (opened, closed, synchronized, etc.).

**Payload Example:**

```json
{
  "action": "opened",
  "pull_request": {
    "number": 123,
    "title": "Add new feature",
    "user": {
      "login": "username"
    },
    "base": {
      "repo": {
        "full_name": "org/repo"
      }
    },
    "html_url": "https://github.com/org/repo/pull/123"
  }
}
```

**Discord Message:**
- **Channel:** `prs`
- **Title:** `PR {action}: #{number} {title}`
- **Description:** `{user} → {repo}\n{url}`

##### check_suite

Handles CI/CD check suite events.

**Payload Example:**

```json
{
  "check_suite": {
    "status": "completed",
    "conclusion": "success",
    "app": {
      "name": "GitHub Actions"
    }
  }
}
```

**Discord Message:**
- **Channel:** `deployments`
- **Title:** `Checks {status}`
- **Description:** `{app_name} → {conclusion}`

##### push

Handles push events to branches.

**Payload Example:**

```json
{
  "ref": "refs/heads/main",
  "repository": {
    "full_name": "org/repo"
  },
  "compare": "https://github.com/org/repo/compare/abc...def"
}
```

**Discord Message:**
- **Channel:** `deployments`
- **Title:** `Push: {ref}`
- **Description:** `{repo}\n{compare_url}`

**Response:** `200 OK`

```
ok
```

**Error Responses:**

- `401 Unauthorized`: Invalid HMAC signature

---

## Refinory Orchestrator API

**Base URL:** `http://localhost:8085`  
**Service:** AI-powered architecture orchestration engine  
**Technology:** Express + JavaScript

### Overview

The Refinory Orchestrator manages AI expert teams for software architecture design and review. It coordinates multiple AI experts with different specialties to collaboratively design systems.

### Configuration

Environment variables:
- `REFINORY_PORT`: Server port (default: 8085)

### Endpoints

#### GET /health

Health check endpoint.

**Response:** `200 OK`

```json
{
  "status": "healthy",
  "timestamp": "2025-12-22T22:00:00Z",
  "version": "1.0.0",
  "config": {
    "experts": 10,
    "strategy": "parallel",
    "gpu": false
  }
}
```

---

#### GET /config

Get Refinory configuration.

**Response:** `200 OK`

```json
{
  "experts": {
    "team": [
      {"name": "frontend"},
      {"name": "backend"}
    ],
    "orchestration": {
      "strategy": "parallel"
    }
  },
  "policies": {},
  "runtime": {
    "gpu": false,
    "workers": 4
  }
}
```

---

#### POST /requests

Create a new architecture request.

**Request Body:**

```json
{
  "project": "new-microservice",
  "description": "Design a scalable user authentication service",
  "requester": "john.doe@example.com",
  "experts": ["backend", "security", "devops"]
}
```

**Request Fields:**
- `project` (required): Project identifier
- `description` (required): Architecture request description
- `requester` (required): Email or ID of requester
- `experts` (optional): Array of expert names to involve (auto-selected if not provided)

**Response:** `201 Created`

```json
{
  "request_id": "req_abc123",
  "status": "created",
  "message": "Architecture request submitted to expert team"
}
```

**Error Responses:**

- `400 Bad Request`: Missing required fields
- `500 Internal Server Error`: Request creation failed

---

#### GET /requests/:id

Get status of an architecture request.

**Parameters:**
- `id`: Request ID

**Response:** `200 OK`

```json
{
  "request_id": "req_abc123",
  "status": "in_progress",
  "project": "new-microservice",
  "description": "Design a scalable user authentication service",
  "requester": "john.doe@example.com",
  "experts": ["backend", "security", "devops"],
  "created_at": "2025-12-22T22:00:00Z",
  "updated_at": "2025-12-22T22:05:00Z",
  "artifacts": ["architecture.md", "diagram.svg"]
}
```

**Error Responses:**

- `404 Not Found`: Request ID not found

---

#### GET /requests

List all architecture requests with optional filtering.

**Query Parameters:**
- `status`: Filter by status (e.g., `created`, `in_progress`, `completed`)
- `requester`: Filter by requester email

**Response:** `200 OK`

```json
{
  "requests": [
    {
      "request_id": "req_abc123",
      "status": "in_progress",
      "project": "new-microservice",
      "created_at": "2025-12-22T22:00:00Z"
    }
  ],
  "count": 1,
  "filters": {
    "status": "in_progress",
    "requester": null
  }
}
```

---

#### GET /requests/:id/artifacts

Get artifacts produced by the architecture request.

**Parameters:**
- `id`: Request ID

**Response:** `200 OK`

```json
{
  "artifacts": [
    {
      "name": "architecture.md",
      "url": "/artifacts/req_abc123/architecture.md",
      "type": "md",
      "size": 15234,
      "created_at": "2025-12-22T22:10:00Z"
    },
    {
      "name": "diagram.svg",
      "url": "/artifacts/req_abc123/diagram.svg",
      "type": "svg",
      "size": 45678,
      "created_at": "2025-12-22T22:12:00Z"
    }
  ]
}
```

**Error Responses:**

- `404 Not Found`: Request ID not found

---

#### GET /experts

Get status of all experts in the team.

**Response:** `200 OK`

```json
{
  "experts": [
    {
      "name": "frontend",
      "status": "available",
      "specialties": ["React", "Vue", "Angular", "TypeScript", "CSS", "UX/UI"],
      "active_requests": 2
    },
    {
      "name": "backend",
      "status": "available",
      "specialties": ["Node.js", "Python", "Go", "Rust", "APIs", "Microservices"],
      "active_requests": 3
    }
  ],
  "orchestration": {
    "strategy": "parallel"
  }
}
```

---

#### POST /requests/:id/feedback

Submit expert feedback for a request (for human-in-the-loop workflows).

**Parameters:**
- `id`: Request ID

**Request Body:**

```json
{
  "expert": "security",
  "feedback": "Consider implementing OAuth 2.0 with PKCE",
  "approved": true
}
```

**Request Fields:**
- `expert` (required): Expert name providing feedback
- `feedback` (required): Feedback text
- `approved` (required): Whether the expert approves

**Response:** `200 OK`

```json
{
  "message": "Feedback recorded",
  "expert": "security",
  "approved": true
}
```

---

#### GET /metrics

Prometheus metrics endpoint.

**Response:** `200 OK` (Content-Type: `text/plain`)

```
# HELP refinory_requests_total Total number of architecture requests
# TYPE refinory_requests_total counter
refinory_requests_total{status="created"} 12

# HELP refinory_experts_active Number of active experts
# TYPE refinory_experts_active gauge  
refinory_experts_active 10

# HELP refinory_processing_duration_seconds Time spent processing requests
# TYPE refinory_processing_duration_seconds histogram
refinory_processing_duration_seconds_bucket{le="10"} 5
refinory_processing_duration_seconds_bucket{le="30"} 8
refinory_processing_duration_seconds_bucket{le="60"} 10
refinory_processing_duration_seconds_bucket{le="+Inf"} 12
refinory_processing_duration_seconds_sum 240
refinory_processing_duration_seconds_count 12
```

---

## Discord Bot Commands

**Service:** Discord bot for DevOps control plane  
**Technology:** Discord.js + TypeScript

### Overview

The Discord bot provides slash commands for managing services, deployments, and infrastructure directly from Discord.

### Authentication

Bot requires a Discord application token and must be invited to your server with appropriate permissions.

### Configuration

Environment variables:
- `DISCORD_TOKEN`: Discord bot token
- `APP_ID`: Discord application ID
- Control API configuration from `discovery.yml`

### Commands

#### /status

Get status of a service.

**Parameters:**
- `service` (required): Service name

**Usage:**
```
/status service:event-gateway
```

**Response:**
```
Status: event-gateway
state: running
version: 1.2.3
```

---

#### /logs

Tail logs from a service.

**Parameters:**
- `service` (required): Service name
- `tail` (optional): Number of lines to tail (default: 200)

**Usage:**
```
/logs service:discord-bot tail:100
```

**Response:**
```
[2025-12-22T22:00:00] INFO: Bot started
[2025-12-22T22:00:01] INFO: Commands registered
...
```

---

#### /deploy

Deploy a tagged version to an environment.

**Parameters:**
- `env` (required): Environment (`dev`, `staging`, `prod`)
- `tag` (required): Git tag or version to deploy

**Usage:**
```
/deploy env:staging tag:v1.2.3
```

**Response:**
```
Deploy
env: staging
tag: v1.2.3
result: success
```

**Note:** Production deployments may require additional role permissions based on governance configuration.

---

#### /scale

Scale a service to a specific number of replicas.

**Parameters:**
- `service` (required): Service name
- `replicas` (required): Number of replicas

**Usage:**
```
/scale service:event-gateway replicas:3
```

**Response:**
```
Scale
service: event-gateway
replicas: 3
result: success
```

---

## Error Handling

All APIs follow standard HTTP status codes:

- `200 OK`: Successful request
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Authentication failed
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server-side error

Error responses include a JSON body with details:

```json
{
  "error": "Error description",
  "timestamp": "2025-12-22T22:00:00Z"
}
```

---

## Rate Limiting

Currently, no rate limiting is enforced. In production, implement rate limiting on all public endpoints:

- RECON RAG API: 100 requests per minute per IP
- Event Gateway: 1000 webhooks per hour per repository
- Refinory API: 50 requests per minute per requester

---

## Monitoring

All APIs expose Prometheus metrics at `/metrics` endpoints for monitoring:

- Request counts by status
- Request duration histograms
- Active connections/requests
- Service-specific metrics

Configure Prometheus to scrape these endpoints for observability.

---

## Security Best Practices

1. **Authentication**: Implement bearer token authentication for all APIs in production
2. **HTTPS**: Use TLS/SSL for all API endpoints
3. **HMAC Verification**: Event Gateway verifies GitHub webhook signatures
4. **Input Validation**: All APIs validate input parameters
5. **Rate Limiting**: Implement rate limiting to prevent abuse
6. **CORS**: Configure CORS policies appropriately for your environment
7. **Secret Management**: Use Vault or similar for managing secrets

---

## Getting Started

### Starting Services

```bash
# Start RECON RAG API
cd recon/retriever
python3 api.py

# Start Event Gateway
npm run dev

# Start Discord Bot
npm run bot

# Start Refinory Orchestrator
node src/refinory/orchestrator.js
```

### Testing APIs

```bash
# Test RECON RAG API
curl http://localhost:7000/health
curl -X POST http://localhost:7000/query \
  -H "Content-Type: application/json" \
  -d '{"q": "How does authentication work?", "k": 5}'

# Test Refinory API
curl http://localhost:8085/health
curl -X POST http://localhost:8085/requests \
  -H "Content-Type: application/json" \
  -d '{
    "project": "test-project",
    "description": "Test architecture request",
    "requester": "test@example.com"
  }'
```

---

## Interactive API Documentation

- **RECON RAG API**: Access Swagger UI at `http://localhost:7000/docs`
- **Event Gateway**: API documentation available in this file
- **Refinory Orchestrator**: API documentation available in this file

---

## Support

For issues, questions, or contributions:
- **Issues**: [GitHub Issues](https://github.com/Strategickhaos-Swarm-Intelligence/sovereignty-architecture/issues)
- **Discord**: [Strategickhaos Discord Server](https://discord.gg/strategickhaos)
- **Documentation**: [Wiki](https://wiki.strategickhaos.internal)

---

**Built with 🔥 by the Strategickhaos Swarm Intelligence collective**

*Empowering sovereign digital infrastructure through comprehensive API access*
