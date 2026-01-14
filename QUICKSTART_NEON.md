# Quick Start: Neon Database Deployment

Get your Sovereignty Architecture running with Neon serverless PostgreSQL in under 5 minutes.

## Prerequisites

- Docker and Docker Compose installed
- A Neon account ([sign up free](https://neon.tech))
- Git installed

## Step-by-Step Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git
cd Sovereignty-Architecture-Elevator-Pitch-
```

### 2. Create Neon Database

1. Go to [Neon Console](https://console.neon.tech/app/org-snowy-moon-53031065/projects)
2. Click **"Create Project"**
3. Name it `sovereignty-architecture`
4. Select your preferred region
5. Click **"Create"**

### 3. Enable pgvector Extension

In the Neon SQL Editor, run:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

Click **"Run"** to execute.

### 4. Get Your Connection String

1. In your Neon project, click **"Connection Details"**
2. Copy the connection string (looks like):
   ```
   postgresql://user:password@ep-xxx-xxx.region.neon.tech/dbname?sslmode=require
   ```

### 5. Configure Environment

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Edit `.env` and set your Neon connection string:

```bash
# Replace with your actual Neon connection string
DATABASE_URL=postgresql://user:password@ep-xxx-xxx.region.neon.tech/dbname?sslmode=require

# Optional: Discord integration
DISCORD_TOKEN=your_discord_bot_token_here
DISCORD_GUILD_ID=your_discord_guild_id_here

# Optional: AI features
OPENAI_API_KEY=sk-your_openai_key_here

# Optional: GitHub integration
GITHUB_TOKEN=your_github_token_here
```

### 6. Test Database Connection

Verify your Neon connection works:

```bash
# Install dependencies (if not already installed)
pip install asyncpg

# Test the connection
python test_neon_connection.py
```

You should see:
```
✅ Successfully connected to database
✅ pgvector extension is installed
✅ All tests passed! Neon database is ready to use.
```

### 7. Deploy with Docker Compose

Start all services using the Neon configuration:

```bash
docker-compose -f docker-compose.neon.yml up -d
```

### 8. Verify Deployment

Check that services are running:

```bash
docker-compose -f docker-compose.neon.yml ps
```

Check the logs:

```bash
# API logs
docker-compose -f docker-compose.neon.yml logs refinory-api

# Look for "Database initialized successfully"
docker-compose -f docker-compose.neon.yml logs refinory-api | grep "Database initialized"
```

### 9. Access the Services

- **Refinory API**: http://localhost:8085
- **Grafana Dashboard**: http://localhost:3001 (admin/refinory123)
- **Prometheus**: http://localhost:9090
- **Qdrant UI**: http://localhost:3002

Test the API:

```bash
curl http://localhost:8085/health
```

## Verify Everything is Working

### Check API Health

```bash
curl http://localhost:8085/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "version": "1.0.0"
}
```

### Check Database Schema

The Refinory system automatically creates the required tables. Verify in the Neon SQL Editor:

```sql
SELECT tablename FROM pg_tables 
WHERE schemaname = 'public' 
ORDER BY tablename;
```

You should see tables like:
- `architecture_requests`
- `expert_tasks`
- `architecture_artifacts`
- `architecture_embeddings`

## What's Next?

### Explore the Dashboard

Open Grafana at http://localhost:3001:
- Username: `admin`
- Password: `refinory123`

### Create Your First Architecture Request

```bash
curl -X POST http://localhost:8085/api/v1/architecture/requests \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "My First Project",
    "description": "A sample architecture request",
    "requirements": ["scalable", "secure"]
  }'
```

### Enable Discord Integration

1. Create a Discord bot ([guide](https://discord.com/developers/applications))
2. Add bot token to `.env`:
   ```bash
   DISCORD_TOKEN=your_bot_token_here
   DISCORD_GUILD_ID=your_server_id_here
   ```
3. Restart services:
   ```bash
   docker-compose -f docker-compose.neon.yml restart
   ```

## Development with Neon Branches

Neon's branching feature is perfect for development:

### Create a Development Branch

1. In Neon Console, go to **"Branches"**
2. Click **"Create Branch"**
3. Name it `development`
4. Copy the new connection string

### Use Development Branch

```bash
# In your development environment
export DATABASE_URL='postgresql://user:password@ep-dev-xxx.region.neon.tech/dbname?sslmode=require'

docker-compose -f docker-compose.neon.yml up -d
```

Now you have an isolated development database!

## Troubleshooting

### Connection Timeout

**Problem**: `Cannot connect to database: connection timeout`

**Solution**: Neon auto-suspends inactive databases. Wait 5-10 seconds and try again. The database will wake up automatically.

### SSL Error

**Problem**: `SSL connection error`

**Solution**: Ensure your connection string includes `?sslmode=require`:
```
postgresql://...?sslmode=require
```

### pgvector Not Found

**Problem**: `extension "vector" does not exist`

**Solution**: Run this in Neon SQL Editor:
```sql
CREATE EXTENSION vector;
```

### Schema Creation Failed

**Problem**: Tables not created automatically

**Solution**: Check API logs and manually create schema if needed:
```bash
docker-compose -f docker-compose.neon.yml logs refinory-api | grep -i error
```

## Stopping Services

```bash
docker-compose -f docker-compose.neon.yml down
```

This stops all containers but keeps your Neon database intact.

## Clean Up

To remove all local containers and volumes:

```bash
docker-compose -f docker-compose.neon.yml down -v
```

Note: This does NOT delete your Neon database. To delete the Neon database, go to the Neon Console.

## Getting Help

- **Documentation**: [NEON_DATABASE_SETUP.md](./NEON_DATABASE_SETUP.md)
- **Neon Support**: [Discord](https://discord.gg/neon)
- **Project Issues**: [GitHub Issues](https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/issues)

## Cost Estimate

Neon's free tier includes:
- ✅ 10 GB storage
- ✅ Unlimited compute hours
- ✅ 1 project with up to 10 branches
- ✅ Auto-suspend after 5 minutes of inactivity

This is perfect for development and small deployments. For production, consider the Pro tier for:
- More storage
- Better performance
- Longer history retention
- Priority support

---

**That's it!** You now have a fully functional Sovereignty Architecture running on Neon serverless PostgreSQL. 🎉

Ready to build something amazing? Check out the [main README](./README.md) for more features and integrations.
