# Integration Examples

Examples for integrating the Neon database with various Strategickhaos Empire systems.

## Table of Contents

1. [Kubernetes Node Heartbeats](#kubernetes-node-heartbeats)
2. [FlameLang Compiler Integration](#flamelang-compiler-integration)
3. [Legion of Minds Session Logging](#legion-of-minds-session-logging)
4. [SAGCO Task Queue](#sagco-task-queue)
5. [Discord Bot Integration](#discord-bot-integration)
6. [GitHub Actions Integration](#github-actions-integration)
7. [Grafana Dashboard](#grafana-dashboard)

---

## Kubernetes Node Heartbeats

Send periodic heartbeats from Kubernetes nodes to track cluster health.

### Node.js Example (DaemonSet)

```javascript
import pkg from 'pg';
const { Client } = pkg;
import os from 'os';

const DATABASE_URL = process.env.DATABASE_URL;
const NODE_ID = process.env.NODE_ID || 'INFRA-001';

async function sendHeartbeat() {
  const client = new Client({
    connectionString: DATABASE_URL,
    ssl: { rejectUnauthorized: false }
  });

  try {
    await client.connect();
    
    const cpuUsage = (os.loadavg()[0] / os.cpus().length) * 100;
    const totalMem = os.totalmem();
    const freeMem = os.freemem();
    const ramUsage = ((totalMem - freeMem) / totalMem) * 100;
    
    await client.query(`
      INSERT INTO node_metrics (node_id, cpu_usage, ram_usage, disk_usage, timestamp)
      VALUES ($1, $2, $3, $4, NOW())
    `, [NODE_ID, cpuUsage.toFixed(2), ramUsage.toFixed(2), 0]);
    
    console.log(`✅ Heartbeat sent for ${NODE_ID}`);
    
  } catch (error) {
    console.error('❌ Heartbeat failed:', error.message);
  } finally {
    await client.end();
  }
}

// Send heartbeat every 60 seconds
setInterval(sendHeartbeat, 60000);
sendHeartbeat(); // Initial heartbeat
```

### Kubernetes CronJob

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: node-heartbeat
spec:
  schedule: "*/1 * * * *"  # Every minute
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: heartbeat
            image: postgres:15-alpine
            env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: neon-credentials
                  key: database-url
            - name: NODE_ID
              valueFrom:
                fieldRef:
                  fieldPath: spec.nodeName
            command:
            - sh
            - -c
            - |
              psql "$DATABASE_URL" -c "
                INSERT INTO node_metrics (node_id, cpu_usage, ram_usage, timestamp)
                VALUES ('K8S-\${NODE_ID}', 0, 0, NOW());
              "
          restartPolicy: OnFailure
```

---

## FlameLang Compiler Integration

Log compilation runs and transformation stages.

### Python Example

```python
import psycopg2
import os
import time
from datetime import datetime

DATABASE_URL = os.getenv('DATABASE_URL')

class FlameLangLogger:
    def __init__(self):
        self.conn = psycopg2.connect(DATABASE_URL)
        self.cursor = self.conn.cursor()
        self.run_id = None
    
    def start_compilation(self, source_file):
        """Start a new compilation run"""
        self.run_id = f"RUN-{int(time.time())}"
        self.start_time = time.time()
        
        print(f"🔥 Starting compilation: {self.run_id}")
        return self.run_id
    
    def log_stage(self, stage, status, details=None):
        """Log a transformation stage"""
        self.cursor.execute("""
            INSERT INTO transformation_logs (run_id, stage, status, details)
            VALUES (%s, %s, %s, %s)
        """, (self.run_id, stage, status, details))
        self.conn.commit()
        
        print(f"  {stage}: {status}")
    
    def end_compilation(self, source_file, success, error_count=0, warning_count=0):
        """Complete the compilation run"""
        execution_time = int((time.time() - self.start_time) * 1000)
        
        self.cursor.execute("""
            INSERT INTO compilation_runs 
            (run_id, source_file, success, error_count, warning_count, execution_time_ms)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (self.run_id, source_file, success, error_count, warning_count, execution_time))
        self.conn.commit()
        
        status = "✅" if success else "❌"
        print(f"{status} Compilation complete: {execution_time}ms")
    
    def close(self):
        self.cursor.close()
        self.conn.close()

# Usage example
logger = FlameLangLogger()
run_id = logger.start_compilation("example.flame")

try:
    logger.log_stage("lexer", "SUCCESS")
    logger.log_stage("parser", "SUCCESS")
    logger.log_stage("transformer", "SUCCESS")
    logger.log_stage("codegen", "SUCCESS")
    
    logger.end_compilation("example.flame", True, 0, 0)
except Exception as e:
    logger.log_stage("parser", "ERROR", str(e))
    logger.end_compilation("example.flame", False, 1, 0)
finally:
    logger.close()
```

---

## Legion of Minds Session Logging

Log AI council sessions and consensus voting.

### Node.js Example

```javascript
import pkg from 'pg';
const { Client } = pkg;

class LegionLogger {
  constructor(databaseUrl) {
    this.client = new Client({
      connectionString: databaseUrl,
      ssl: { rejectUnauthorized: false }
    });
  }

  async connect() {
    await this.client.connect();
  }

  async startSession(topic) {
    const sessionId = `SESSION-${Date.now()}`;
    
    await this.client.query(`
      INSERT INTO council_sessions (session_id, topic, session_date)
      VALUES ($1, $2, NOW())
    `, [sessionId, topic]);
    
    console.log(`🤖 Legion session started: ${sessionId}`);
    console.log(`   Topic: ${topic}`);
    
    return sessionId;
  }

  async recordVote(sessionId, councilMemberId, vote, reasoning) {
    await this.client.query(`
      INSERT INTO model_votes (session_id, council_member_id, vote, reasoning)
      VALUES ($1, $2, $3, $4)
    `, [sessionId, councilMemberId, vote, reasoning]);
    
    console.log(`   ${councilMemberId}: ${vote}`);
  }

  async recordConsensus(sessionId, decision, votes) {
    await this.client.query(`
      INSERT INTO consensus_outcomes 
      (session_id, decision, vote_count_approve, vote_count_reject, vote_count_abstain)
      VALUES ($1, $2, $3, $4, $5)
    `, [sessionId, decision, votes.approve, votes.reject, votes.abstain]);
    
    // Update session
    await this.client.query(`
      UPDATE council_sessions
      SET consensus_reached = $1
      WHERE session_id = $2
    `, [decision !== 'DEFERRED', sessionId]);
    
    console.log(`✅ Consensus: ${decision}`);
    console.log(`   Approve: ${votes.approve}, Reject: ${votes.reject}, Abstain: ${votes.abstain}`);
  }

  async close() {
    await this.client.end();
  }
}

// Usage example
async function runLegionSession() {
  const logger = new LegionLogger(process.env.DATABASE_URL);
  await logger.connect();
  
  const sessionId = await logger.startSession('Deploy new security patch');
  
  await logger.recordVote(sessionId, 'AI-001', 'APPROVE', 'Security patch addresses CVE-2024-1234');
  await logger.recordVote(sessionId, 'AI-002', 'APPROVE', 'No conflicts with existing systems');
  await logger.recordVote(sessionId, 'AI-003', 'APPROVE', 'Complies with security policy');
  await logger.recordVote(sessionId, 'AI-004', 'APPROVE', 'Threat analysis confirms necessity');
  await logger.recordVote(sessionId, 'AI-005', 'ABSTAIN', 'Insufficient regulatory context');
  
  await logger.recordConsensus(sessionId, 'APPROVED', {
    approve: 4,
    reject: 0,
    abstain: 1
  });
  
  await logger.close();
}

runLegionSession();
```

---

## SAGCO Task Queue

Manage distributed task orchestration.

### Python Example

```python
import psycopg2
import json
import os
from datetime import datetime

DATABASE_URL = os.getenv('DATABASE_URL')

class SAGCOQueue:
    def __init__(self):
        self.conn = psycopg2.connect(DATABASE_URL)
        self.cursor = self.conn.cursor()
    
    def enqueue(self, task_type, payload, priority=5):
        """Add a task to the queue"""
        task_id = f"TASK-{int(datetime.now().timestamp())}"
        
        self.cursor.execute("""
            INSERT INTO task_queue (task_id, task_type, priority, status, payload)
            VALUES (%s, %s, %s, 'PENDING', %s)
        """, (task_id, task_type, priority, json.dumps(payload)))
        self.conn.commit()
        
        print(f"📋 Task queued: {task_id} ({task_type})")
        return task_id
    
    def dequeue(self, node_id):
        """Get next task for processing"""
        self.cursor.execute("""
            UPDATE task_queue
            SET status = 'IN_PROGRESS',
                assigned_node = %s
            WHERE id = (
                SELECT id FROM task_queue
                WHERE status = 'PENDING'
                ORDER BY priority DESC, created_at ASC
                LIMIT 1
                FOR UPDATE SKIP LOCKED
            )
            RETURNING task_id, task_type, payload
        """, (node_id,))
        
        task = self.cursor.fetchone()
        self.conn.commit()
        
        if task:
            print(f"🎯 Task assigned to {node_id}: {task[0]}")
            return {
                'task_id': task[0],
                'task_type': task[1],
                'payload': json.loads(task[2])
            }
        return None
    
    def complete(self, task_id, success=True):
        """Mark task as completed"""
        status = 'COMPLETED' if success else 'FAILED'
        
        self.cursor.execute("""
            UPDATE task_queue
            SET status = %s,
                completed_at = NOW()
            WHERE task_id = %s
        """, (status, task_id))
        self.conn.commit()
        
        symbol = "✅" if success else "❌"
        print(f"{symbol} Task {status.lower()}: {task_id}")
    
    def close(self):
        self.cursor.close()
        self.conn.close()

# Usage example
queue = SAGCOQueue()

# Enqueue tasks
queue.enqueue('BUILD', {'repo': 'strategickhaos/core', 'branch': 'main'}, priority=8)
queue.enqueue('TEST', {'suite': 'integration'}, priority=6)
queue.enqueue('DEPLOY', {'environment': 'staging'}, priority=10)

# Dequeue and process
task = queue.dequeue('ATHENA101')
if task:
    print(f"Processing: {task['task_type']}")
    # ... do work ...
    queue.complete(task['task_id'], success=True)

queue.close()
```

---

## Discord Bot Integration

Query database from Discord bot for status commands.

### JavaScript Example

```javascript
import { Client, GatewayIntentBits } from 'discord.js';
import pkg from 'pg';
const { Client: PgClient } = pkg;

const discord = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages] });

async function queryDatabase(query, params = []) {
  const client = new PgClient({
    connectionString: process.env.DATABASE_URL,
    ssl: { rejectUnauthorized: false }
  });
  
  await client.connect();
  const result = await client.query(query, params);
  await client.end();
  
  return result;
}

discord.on('messageCreate', async (message) => {
  if (message.author.bot) return;
  
  // !status command
  if (message.content === '!status') {
    try {
      const inventions = await queryDatabase('SELECT COUNT(*) FROM inventions');
      const entities = await queryDatabase('SELECT COUNT(*) FROM legal_entities');
      const nodes = await queryDatabase('SELECT COUNT(*) FROM cluster_nodes WHERE status = $1', ['ONLINE']);
      
      message.reply(
        `📊 **Empire Status**\n` +
        `Inventions: ${inventions.rows[0].count}\n` +
        `Legal Entities: ${entities.rows[0].count}\n` +
        `Nodes Online: ${nodes.rows[0].count}`
      );
    } catch (error) {
      message.reply('❌ Database error');
    }
  }
  
  // !inventions command
  if (message.content.startsWith('!inventions')) {
    try {
      const result = await queryDatabase(`
        SELECT invention_id, title, status
        FROM inventions
        ORDER BY invention_id
        LIMIT 10
      `);
      
      let response = '📚 **Recent Inventions**\n```\n';
      result.rows.forEach(row => {
        response += `${row.invention_id}: ${row.title} [${row.status}]\n`;
      });
      response += '```';
      
      message.reply(response);
    } catch (error) {
      message.reply('❌ Database error');
    }
  }
});

discord.login(process.env.DISCORD_BOT_TOKEN);
```

---

## GitHub Actions Integration

Log deployments and CI events to the database.

### GitHub Actions Workflow

```yaml
name: Deploy and Log to Neon

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Log deployment event
        env:
          DATABASE_URL: ${{ secrets.NEON_DATABASE_URL }}
        run: |
          psql "$DATABASE_URL" -c "
            INSERT INTO swarm_events (event_id, event_type, source, description, metadata)
            VALUES (
              'EVT-${{ github.run_id }}',
              'GITHUB_DEPLOY',
              'GitHub Actions',
              'Deployment triggered by ${{ github.actor }}',
              '{\"repo\": \"${{ github.repository }}\", \"sha\": \"${{ github.sha }}\"}'::jsonb
            );
          "
      
      - name: Build and deploy
        run: |
          # Your deployment steps here
          echo "Deploying..."
      
      - name: Log success
        if: success()
        env:
          DATABASE_URL: ${{ secrets.NEON_DATABASE_URL }}
        run: |
          psql "$DATABASE_URL" -c "
            UPDATE swarm_events
            SET metadata = metadata || '{\"status\": \"SUCCESS\"}'::jsonb
            WHERE event_id = 'EVT-${{ github.run_id }}';
          "
```

---

## Grafana Dashboard

Query Neon database for visualization in Grafana.

### PostgreSQL Data Source Configuration

1. In Grafana, add a PostgreSQL data source
2. Host: `ep-shiny-dream-a49u5n6p.us-east-1.aws.neon.tech`
3. Database: `neondb`
4. User: `neondb_owner`
5. Password: `[your password]`
6. SSL Mode: `require`

### Example Panel Queries

**Node Metrics Over Time:**
```sql
SELECT
  timestamp AS time,
  node_id,
  cpu_usage,
  ram_usage
FROM node_metrics
WHERE $__timeFilter(timestamp)
ORDER BY timestamp
```

**Invention Status Distribution:**
```sql
SELECT
  status,
  COUNT(*) as count
FROM inventions
GROUP BY status
```

**Task Queue Backlog:**
```sql
SELECT
  task_type,
  COUNT(*) as pending_tasks
FROM task_queue
WHERE status = 'PENDING'
GROUP BY task_type
```

**Daily Event Volume:**
```sql
SELECT
  DATE(created_at) as date,
  event_type,
  COUNT(*) as count
FROM swarm_events
WHERE $__timeFilter(created_at)
GROUP BY DATE(created_at), event_type
ORDER BY date DESC
```

---

## Environment Variables

All examples require:

```bash
export DATABASE_URL="postgresql://neondb_owner:password@ep-shiny-dream-a49u5n6p.us-east-1.aws.neon.tech/neondb?sslmode=require"
```

For Kubernetes secrets:

```bash
kubectl create secret generic neon-credentials \
  --from-literal=database-url="postgresql://..."
```

---

## Testing Integrations

Test each integration:

```bash
# Node.js examples
node heartbeat-example.js

# Python examples
python3 flamelang-logger.py

# Database queries
psql "$DATABASE_URL" -c "SELECT COUNT(*) FROM node_metrics;"
```

---

## Security Best Practices

1. **Never commit credentials** - Use environment variables or secrets management
2. **Use connection pooling** for high-concurrency workloads
3. **Implement retry logic** for transient network failures
4. **Monitor query performance** - Use Neon dashboard to identify slow queries
5. **Use read-only roles** for reporting/visualization

---

*For more examples and documentation, see [NEON_DATABASE.md](./NEON_DATABASE.md)*
