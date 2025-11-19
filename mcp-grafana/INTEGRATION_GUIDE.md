# MCP Grafana Integration Guide

## Overview

This guide explains how the MCP (Model Context Protocol) Grafana server integrates with the Sovereignty Architecture and how to use it effectively.

## What is MCP?

Model Context Protocol (MCP) is an open protocol developed by Anthropic that standardizes how AI assistants connect to data sources and tools. It enables:

- **Standardized Integration**: AI assistants can connect to various tools using a common protocol
- **Secure Access**: Tools expose only authorized capabilities through well-defined interfaces
- **Real-time Data**: AI assistants can query live data sources rather than relying on stale training data

## Architecture Integration

The MCP Grafana server fits into the Sovereignty Architecture as follows:

```
┌─────────────────┐
│   AI Assistant  │ (Claude Desktop, etc.)
│  (Claude, GPT)  │
└────────┬────────┘
         │ MCP Protocol
         │
┌────────▼────────┐
│  MCP Grafana    │
│     Server      │
└────────┬────────┘
         │ HTTP/REST
         │
┌────────▼────────┐
│     Grafana     │
│   (Port 3000)   │
└────────┬────────┘
         │
    ┌────┴────┬─────────┬──────────┐
    │         │         │          │
┌───▼───┐ ┌──▼──┐  ┌───▼────┐ ┌──▼──────┐
│Prometheus│ │Loki│  │Jaeger│ │Alertmgr│
└─────────┘ └─────┘  └────────┘ └─────────┘
```

## Deployment Options

### Option 1: Docker Compose (Recommended)

Deploy alongside existing monitoring stack:

```bash
# Start all services including MCP Grafana
docker-compose -f docker-compose-scaffold.yml -f docker-compose.mcp.yml up -d
```

### Option 2: Standalone with Claude Desktop

For local development with Claude Desktop:

```bash
# Build and run locally
cd mcp-grafana
npm install
npm run build
npm start
```

Then configure Claude Desktop (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "grafana": {
      "command": "node",
      "args": ["/path/to/mcp-grafana/dist/index.js"],
      "env": {
        "GRAFANA_URL": "http://localhost:3000",
        "GRAFANA_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### Option 3: Kubernetes Deployment

For production Kubernetes deployments:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mcp-grafana-server
  namespace: monitoring
spec:
  replicas: 2
  selector:
    matchLabels:
      app: mcp-grafana
  template:
    metadata:
      labels:
        app: mcp-grafana
    spec:
      containers:
      - name: mcp-grafana
        image: mcp-grafana-server:latest
        env:
        - name: GRAFANA_URL
          value: "http://grafana.monitoring.svc.cluster.local:3000"
        - name: GRAFANA_API_KEY
          valueFrom:
            secretKeyRef:
              name: grafana-api-key
              key: api-key
        stdin: true
        tty: true
```

## Usage Examples

### Example 1: Check System Health

**User:** "Is Grafana healthy?"

**AI Assistant uses:** `check_health` tool

**Result:** Returns Grafana health status

### Example 2: List Available Dashboards

**User:** "Show me all available dashboards"

**AI Assistant uses:** `list_dashboards` tool

**Result:** Lists all dashboards with their UIDs, titles, and URLs

### Example 3: Query Metrics

**User:** "What's the current CPU usage?"

**AI Assistant uses:** `query_metrics` tool with PromQL query

**Result:** Returns current CPU metrics from Prometheus

### Example 4: Check Active Alerts

**User:** "Are there any active alerts?"

**AI Assistant uses:** `list_alerts` tool

**Result:** Lists all active Grafana alerts with severity and details

### Example 5: Dashboard Analysis

**User:** "Show me the details of the 'kubernetes-cluster' dashboard"

**AI Assistant uses:** `get_dashboard` tool with UID

**Result:** Returns full dashboard configuration including panels and queries

## Security Considerations

### API Key Management

1. **Generate a Read-Only API Key:**
   - Navigate to Grafana → Configuration → API Keys
   - Create a new key with "Viewer" role
   - Store securely in environment variables or secrets management

2. **Use Kubernetes Secrets:**
   ```bash
   kubectl create secret generic grafana-api-key \
     --from-literal=api-key=your_api_key_here \
     -n monitoring
   ```

3. **Rotate Keys Regularly:**
   - Set expiration dates on API keys
   - Rotate every 90 days minimum
   - Revoke compromised keys immediately

### Network Security

1. **Use Internal DNS:**
   - Connect to Grafana via internal service DNS
   - Avoid exposing Grafana publicly

2. **Apply Network Policies:**
   ```yaml
   apiVersion: networking.k8s.io/v1
   kind: NetworkPolicy
   metadata:
     name: mcp-grafana-policy
   spec:
     podSelector:
       matchLabels:
         app: mcp-grafana
     policyTypes:
     - Egress
     egress:
     - to:
       - podSelector:
           matchLabels:
             app: grafana
       ports:
       - protocol: TCP
         port: 3000
   ```

## Monitoring and Observability

### Logging

The MCP server logs to stderr by default. In production:

```bash
# View logs in Docker
docker logs -f mcp-grafana-server

# View logs in Kubernetes
kubectl logs -f deployment/mcp-grafana-server -n monitoring
```

### Health Checks

Monitor the MCP server health:

```bash
# Check if server is responding
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | docker exec -i mcp-grafana-server node dist/index.js
```

### Metrics Collection

Add Prometheus metrics to track:
- Request count per tool
- Request latency
- Error rates
- API key usage

## Troubleshooting

### Issue: "Connection Refused"

**Solution:**
1. Verify Grafana is running: `curl http://localhost:3000/api/health`
2. Check GRAFANA_URL in environment
3. Ensure network connectivity

### Issue: "Unauthorized"

**Solution:**
1. Verify API key is valid
2. Check API key permissions (needs at least Viewer role)
3. Ensure API key hasn't expired

### Issue: "No Data Returned"

**Solution:**
1. Verify datasources are configured in Grafana
2. Check that metrics exist for queries
3. Ensure appropriate time ranges

### Issue: "MCP Server Not Found"

**Solution:**
1. Verify path in Claude Desktop config
2. Check that dist/index.js exists
3. Ensure Node.js is in PATH

## Advanced Configuration

### Custom Tool Development

To add new MCP tools:

1. Define tool in `tools` array:
```typescript
{
  name: 'custom_tool',
  description: 'Description of what it does',
  inputSchema: {
    type: 'object',
    properties: {
      param1: { type: 'string' }
    }
  }
}
```

2. Add handler in CallToolRequestSchema:
```typescript
case 'custom_tool': {
  const { param1 } = args;
  const result = await customFunction(param1);
  return {
    content: [{ type: 'text', text: JSON.stringify(result) }]
  };
}
```

### Performance Optimization

1. **Caching:** Implement response caching for expensive queries
2. **Rate Limiting:** Add rate limiting to prevent API overload
3. **Connection Pooling:** Use connection pooling for Grafana API
4. **Batch Requests:** Support batching multiple queries

## Integration with Discord Bot

The MCP server can be integrated with the Discord bot:

```typescript
// In Discord bot code
import { MCPClient } from '@modelcontextprotocol/sdk/client';

const mcpClient = new MCPClient({
  transport: new StdioClientTransport({
    command: 'node',
    args: ['./mcp-grafana/dist/index.js'],
    env: {
      GRAFANA_URL: process.env.GRAFANA_URL,
      GRAFANA_API_KEY: process.env.GRAFANA_API_KEY
    }
  })
});

// Use in Discord commands
bot.onCommand('grafana-health', async (interaction) => {
  const result = await mcpClient.callTool('check_health', {});
  await interaction.reply(result);
});
```

## Contributing

To contribute improvements:

1. Fork the repository
2. Make changes to `mcp-grafana/src/index.ts`
3. Test thoroughly with `npm run dev`
4. Build with `npm run build`
5. Submit PR with tests and documentation

## Support

For issues and questions:
- GitHub Issues: https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/issues
- Discord: https://discord.gg/strategickhaos
- Documentation: See main README.md and mcp-grafana/README.md

## References

- [MCP Specification](https://modelcontextprotocol.io)
- [Grafana API Documentation](https://grafana.com/docs/grafana/latest/developers/http_api/)
- [Claude Desktop MCP Setup](https://docs.anthropic.com/claude/docs/model-context-protocol)
- [Prometheus Query Language](https://prometheus.io/docs/prometheus/latest/querying/basics/)
