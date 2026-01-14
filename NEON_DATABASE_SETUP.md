# Neon Database Integration Guide

This guide explains how to integrate Neon's serverless PostgreSQL database with the Sovereignty Architecture project.

## What is Neon?

[Neon](https://neon.tech) is a serverless PostgreSQL database service that provides:
- **Serverless**: Pay only for what you use, with automatic scaling
- **Instant branching**: Create database branches for development and testing
- **pgvector support**: Built-in support for vector embeddings (required for Refinory)
- **High availability**: Automatic backups and point-in-time recovery
- **Fast cold starts**: Sub-second database activation

## Prerequisites

1. A Neon account (sign up at [https://neon.tech](https://neon.tech))
2. Access to the Neon console: [https://console.neon.tech/app/org-snowy-moon-53031065/projects](https://console.neon.tech/app/org-snowy-moon-53031065/projects)

## Setup Instructions

### Step 1: Create a Neon Project

1. Log in to the Neon console
2. Click "Create Project"
3. Choose a project name (e.g., "sovereignty-architecture")
4. Select a region close to your deployment location
5. Click "Create"

### Step 2: Enable pgvector Extension

The Refinory system requires pgvector for vector embeddings. To enable it:

1. In your Neon project, go to the SQL Editor
2. Run the following command:
   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   ```

### Step 3: Get Your Connection String

1. In your Neon project dashboard, click "Connection Details"
2. Copy the connection string (it looks like this):
   ```
   postgresql://user:password@ep-xxx-xxx.region.neon.tech/dbname?sslmode=require
   ```

### Step 4: Configure Environment Variables

Update your `.env` file with the Neon connection string:

```bash
# Neon Database Configuration
DATABASE_URL=postgresql://user:password@ep-xxx-xxx.region.neon.tech/dbname?sslmode=require
DB_HOST=ep-xxx-xxx.region.neon.tech
DB_PORT=5432
DB_DATABASE=your_database_name
DB_USERNAME=your_neon_username
DB_PASSWORD=your_neon_password
```

**Important**: The `DATABASE_URL` takes precedence over individual parameters. If set, it will be used directly.

### Step 5: Deploy with Neon

#### Option A: Using Docker Compose with Neon

Use the Neon-specific docker-compose file:

```bash
# Make sure DATABASE_URL is set in .env
docker-compose -f docker-compose.neon.yml up -d
```

This configuration excludes the local PostgreSQL container and uses your Neon database instead.

#### Option B: Using Kubernetes with Neon

Update the Kubernetes secrets:

```bash
# Create a secret with your Neon connection string
kubectl create secret generic refinory-db-secret \
  --from-literal=database-url='postgresql://user:password@ep-xxx-xxx.region.neon.tech/dbname?sslmode=require' \
  -n refinory
```

Then update your deployment to use the secret:

```yaml
env:
  - name: DATABASE_URL
    valueFrom:
      secretKeyRef:
        name: refinory-db-secret
        key: database-url
```

### Step 6: Initialize Database Schema

The Refinory system will automatically create the required schema on first run. You can verify this by checking the logs:

```bash
# Docker Compose
docker-compose -f docker-compose.neon.yml logs refinory-api | grep "Database initialized"

# Kubernetes
kubectl logs -f deployment/refinory-api -n refinory | grep "Database initialized"
```

## Database Branching for Development

One of Neon's key features is instant database branching. This is useful for:
- Testing schema changes
- Running integration tests
- Creating per-developer environments

### Creating a Branch

1. In the Neon console, go to your project
2. Click "Branches" in the sidebar
3. Click "Create Branch"
4. Choose a parent branch (usually `main`)
5. Give it a name (e.g., `dev`, `staging`, `test-feature`)
6. Click "Create"

### Using a Branch

Each branch has its own connection string. Copy it and use it in your environment:

```bash
# Development branch
DATABASE_URL=postgresql://user:password@ep-dev-xxx.region.neon.tech/dbname?sslmode=require
```

## Connection Pooling

Neon has built-in connection pooling. For applications that need additional pooling, configure the connection pool settings in your `.env`:

```bash
DB_MIN_CONNECTIONS=5
DB_MAX_CONNECTIONS=20
```

## SSL/TLS Configuration

Neon requires SSL connections by default. The connection string includes `?sslmode=require`. Supported SSL modes:

- `require`: Encrypts the connection (default, recommended)
- `verify-ca`: Encrypts and verifies the server certificate
- `verify-full`: Encrypts and verifies the server certificate and hostname

## Performance Optimization

### Connection Settings

For optimal performance with Neon:

```bash
# Recommended pool settings
DB_MIN_CONNECTIONS=5
DB_MAX_CONNECTIONS=20

# Connection timeout (Neon has fast cold starts)
DB_COMMAND_TIMEOUT=60
```

### Indexes

The Refinory database layer automatically creates indexes. For custom queries, consider adding indexes in the Neon SQL Editor:

```sql
CREATE INDEX CONCURRENTLY idx_custom_query ON table_name(column_name);
```

## Monitoring

### Neon Dashboard

Monitor your database in the Neon console:
- Go to your project
- Click "Monitoring" in the sidebar
- View metrics for:
  - Connection count
  - Query performance
  - Storage usage
  - Compute usage

### Application Metrics

The Refinory system exports database metrics to Prometheus. View them in Grafana:

```
http://localhost:3001/dashboards
```

Look for the "Refinory Database" dashboard.

## Backup and Recovery

Neon provides automatic backups:

1. **Point-in-time Recovery**: Restore to any point within the last 7 days (Free tier) or 30 days (Pro tier)
2. **Automated Snapshots**: Daily snapshots are created automatically
3. **Branch from Backup**: Create a branch from any historical point

To restore:
1. Go to "Branches" in the Neon console
2. Click "Create Branch"
3. Select "Restore from history"
4. Choose the timestamp
5. Create the branch

## Migration from Local PostgreSQL to Neon

If you're migrating from local PostgreSQL:

### Step 1: Dump Local Database

```bash
docker-compose exec postgres pg_dump -U refinory refinory > backup.sql
```

### Step 2: Import to Neon

```bash
# Using psql
psql "postgresql://user:password@ep-xxx-xxx.region.neon.tech/dbname?sslmode=require" < backup.sql

# Or using the Neon SQL Editor (for smaller databases)
# Copy and paste the SQL from backup.sql
```

### Step 3: Switch Configuration

Update your `.env` to use the Neon connection string and restart services.

## Troubleshooting

### Connection Refused

- **Check**: Is the connection string correct?
- **Check**: Is your IP allowed? (Neon allows all IPs by default)
- **Check**: Is the database active? (Neon auto-suspends after inactivity)

### SSL Errors

- **Solution**: Ensure `sslmode=require` is in your connection string
- **Check**: Your client supports TLS 1.2+

### Schema Errors

- **Check**: Is pgvector extension enabled? Run:
  ```sql
  CREATE EXTENSION IF NOT EXISTS vector;
  ```

### Performance Issues

- **Check**: Connection pool settings (min/max connections)
- **Check**: Query performance in Neon's monitoring dashboard
- **Consider**: Upgrading to a larger compute size in Neon

## Cost Optimization

Neon's free tier includes:
- 10 GB storage
- Unlimited compute hours (with auto-suspend)
- 1 project with up to 10 branches

To minimize costs:
1. Enable auto-suspend (default: after 5 minutes of inactivity)
2. Delete unused branches
3. Use branches instead of separate databases for testing

## Security Best Practices

1. **Use strong passwords**: Generate passwords with `openssl rand -base64 32`
2. **Rotate credentials**: Change passwords periodically
3. **Use secrets management**: Store `DATABASE_URL` in Kubernetes secrets or Vault
4. **Enable SSL**: Always use `sslmode=require` or higher
5. **Principle of least privilege**: Create separate database users with minimal permissions

## Support and Resources

- **Neon Documentation**: [https://neon.tech/docs](https://neon.tech/docs)
- **Neon Discord**: [https://discord.gg/neon](https://discord.gg/neon)
- **Project Issues**: [GitHub Issues](https://github.com/Strategickhaos-Swarm-Intelligence/sovereignty-architecture/issues)

## Example: Complete Setup

Here's a complete example from scratch:

```bash
# 1. Get your Neon connection string from the console
export DATABASE_URL='postgresql://user:password@ep-xxx-xxx.region.neon.tech/dbname?sslmode=require'

# 2. Update .env file
echo "DATABASE_URL=$DATABASE_URL" >> .env

# 3. Deploy with Neon
docker-compose -f docker-compose.neon.yml up -d

# 4. Verify database connection
docker-compose -f docker-compose.neon.yml logs refinory-api | grep "Database initialized"

# 5. Access the API
curl http://localhost:8085/health
```

Success! Your Sovereignty Architecture is now running with Neon serverless PostgreSQL.
