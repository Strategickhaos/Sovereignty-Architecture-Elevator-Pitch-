// src/event-gateway.js
import express from "express";
import crypto from "crypto";
import { loadConfig, getChannelId } from "./config.js";
import axios from "axios";

const config = loadConfig();
const app = express();
app.use(express.json({ limit: "5mb" }));

const port = process.env.EVENT_GATEWAY_PORT || 8080;
const baseCfg = config.event_gateway;
const hmacKey = process.env.EVENTS_HMAC_KEY;

function verifyHmac(req, rawBody) {
  if (!hmacKey) {
    console.warn("⚠️  HMAC verification disabled (EVENTS_HMAC_KEY not set)");
    return true;
  }

  const headerName = baseCfg.auth?.hmac?.header || "X-Sig";
  const sig = req.headers[headerName.toLowerCase()];
  if (!sig) return false;

  const digest = crypto
    .createHmac("sha256", hmacKey)
    .update(rawBody)
    .digest("hex");

  return sig === digest;
}

// Middleware to capture raw body for HMAC
app.use((req, res, next) => {
  let data = [];
  req.on("data", (chunk) => data.push(chunk));
  req.on("end", () => {
    req.rawBody = Buffer.concat(data);
    try {
      if (data.length && req.headers["content-type"]?.includes("application/json")) {
        req.body = JSON.parse(req.rawBody.toString("utf8"));
      }
    } catch {
      req.body = {};
    }
    next();
  });
});

// Discord webhook poster
async function postToDiscordChannel(channelId, embed) {
  const token = process.env.DISCORD_TOKEN;
  if (!token) {
    console.warn("⚠️  DISCORD_TOKEN not set, skipping Discord post");
    return;
  }

  const payload = {
    embeds: Array.isArray(embed) ? embed : [embed]
  };

  try {
    await axios.post(
      `https://discord.com/api/v10/channels/${channelId}/messages`,
      payload,
      { headers: { Authorization: `Bot ${token}` } }
    );
    console.log(`✅ Posted to Discord channel ${channelId}`);
  } catch (error) {
    console.error(`❌ Failed to post to Discord:`, error.response?.data || error.message);
  }
}

// Health check
app.get("/health", (req, res) => {
  res.json({ 
    status: "healthy", 
    timestamp: new Date().toISOString(),
    config: config.org.name
  });
});

// /event – generic service events
app.post("/event", async (req, res) => {
  console.log("📥 Received /event:", req.body);
  
  if (!verifyHmac(req, req.rawBody || Buffer.from(""))) {
    return res.status(401).send("Invalid signature");
  }

  const event = req.body || {};
  const svc = event.service || "unknown";
  const status = event.status || "info";
  
  const endpointCfg = baseCfg.endpoints.find((e) => e.path === "/event");
  if (!endpointCfg) return res.status(404).send("Endpoint config missing");

  const channelName = endpointCfg.discord_channel;
  const channelId = getChannelId(channelName);
  if (!channelId) {
    console.warn(`⚠️  Channel ID not configured for ${channelName}`);
    return res.status(200).json({ warning: `Channel ${channelName} not configured` });
  }

  // Check if service is allowed
  const allowedServices = endpointCfg.allowed_services || [];
  const isAllowed = allowedServices.some(pattern => {
    if (pattern.endsWith('*')) {
      return svc.startsWith(pattern.slice(0, -1));
    }
    return svc === pattern;
  });

  if (!isAllowed) {
    return res.status(403).send(`Service ${svc} not allowed`);
  }

  const embed = {
    title: `🔔 Service Event: ${svc}`,
    description: event.description || "Service event received",
    color: status === 'success' ? 0x00ff00 : 
           status === 'failure' ? 0xff0000 : 
           status === 'warning' ? 0xffa500 : 0x0099ff,
    fields: [
      { name: "Service", value: svc, inline: true },
      { name: "Status", value: status, inline: true },
      { name: "Source", value: event.source || "API", inline: true }
    ],
    timestamp: new Date().toISOString()
  };

  if (event.repo) embed.fields.push({ name: "Repository", value: event.repo, inline: true });
  if (event.sha) embed.fields.push({ name: "Commit", value: event.sha.substring(0, 8), inline: true });

  await postToDiscordChannel(channelId, embed);
  res.json({ ok: true, channelId });
});

// /alert – alertmanager -> Discord
app.post("/alert", async (req, res) => {
  console.log("🚨 Received /alert:", req.body);
  
  if (!verifyHmac(req, req.rawBody || Buffer.from(""))) {
    return res.status(401).send("Invalid signature");
  }

  const endpointCfg = baseCfg.endpoints.find((e) => e.path === "/alert");
  if (!endpointCfg) return res.status(404).send("Endpoint config missing");

  const channelName = endpointCfg.discord_channel;
  const channelId = getChannelId(channelName);
  if (!channelId) {
    console.warn(`⚠️  Channel ID not configured for ${channelName}`);
    return res.status(200).json({ warning: `Channel ${channelName} not configured` });
  }

  const alerts = req.body?.alerts || [req.body];
  const embeds = alerts.map(alert => ({
    title: `🚨 Alert: ${alert.labels?.alertname || 'Unknown'}`,
    description: alert.annotations?.description || alert.annotations?.summary || "Alert triggered",
    color: alert.status === 'firing' ? 0xff0000 : 0x00ff00,
    fields: [
      { name: "Status", value: alert.status || "unknown", inline: true },
      { name: "Severity", value: alert.labels?.severity || "unknown", inline: true },
      { name: "Instance", value: alert.labels?.instance || "N/A", inline: true }
    ],
    timestamp: new Date().toISOString()
  }));

  await postToDiscordChannel(channelId, embeds.slice(0, 10)); // Limit to 10 embeds
  res.json({ ok: true, alerts: embeds.length });
});

// /git - GitHub webhooks
app.post("/git", async (req, res) => {
  console.log("🐙 Received /git webhook:", req.headers['x-github-event']);
  
  if (!verifyHmac(req, req.rawBody || Buffer.from(""))) {
    return res.status(401).send("Invalid signature");
  }

  const event = req.headers['x-github-event'];
  const payload = req.body;
  
  const gitEndpoint = baseCfg.endpoints.find(e => e.path === "/git");
  if (!gitEndpoint) return res.status(404).send("Git endpoint not configured");

  // Find matching route
  const route = gitEndpoint.routes?.find(r => {
    if (r.event !== event) return false;
    
    if (r.actions && payload.action) {
      return r.actions.includes(payload.action);
    }
    
    if (r.branches && payload.ref) {
      const branch = payload.ref.replace('refs/heads/', '');
      return r.branches.some(pattern => {
        if (pattern.endsWith('*')) {
          return branch.startsWith(pattern.slice(0, -1));
        }
        return branch === pattern;
      });
    }
    
    return true;
  });

  if (!route) {
    return res.status(200).json({ info: `No route configured for ${event}:${payload.action}` });
  }

  const channelId = getChannelId(route.discord_channel);
  if (!channelId) {
    return res.status(200).json({ warning: `Channel ${route.discord_channel} not configured` });
  }

  let embed;
  
  switch (event) {
    case 'pull_request':
      embed = {
        title: `🔄 PR ${payload.action}: ${payload.pull_request.title}`,
        description: payload.pull_request.body?.substring(0, 500) || "No description",
        url: payload.pull_request.html_url,
        color: payload.action === 'opened' ? 0x00ff00 : 
               payload.action === 'closed' && payload.pull_request.merged ? 0x6f42c1 :
               payload.action === 'closed' ? 0x6a737d : 0x0099ff,
        fields: [
          { name: "Repository", value: payload.repository.full_name, inline: true },
          { name: "Author", value: payload.pull_request.user.login, inline: true },
          { name: "Base", value: payload.pull_request.base.ref, inline: true }
        ],
        timestamp: new Date().toISOString()
      };
      break;
      
    case 'push':
      const commits = payload.commits?.slice(0, 5) || [];
      embed = {
        title: `📝 Push to ${payload.ref.replace('refs/heads/', '')}`,
        description: commits.map(c => `• ${c.message.split('\\n')[0]}`).join('\\n'),
        url: payload.compare,
        color: 0x0099ff,
        fields: [
          { name: "Repository", value: payload.repository.full_name, inline: true },
          { name: "Pusher", value: payload.pusher.name, inline: true },
          { name: "Commits", value: commits.length.toString(), inline: true }
        ],
        timestamp: new Date().toISOString()
      };
      break;
      
    case 'check_suite':
      embed = {
        title: `✅ CI ${payload.check_suite.conclusion}: ${payload.check_suite.head_branch}`,
        description: `Check suite ${payload.check_suite.conclusion || 'running'}`,
        url: payload.check_suite.html_url,
        color: payload.check_suite.conclusion === 'success' ? 0x00ff00 : 
               payload.check_suite.conclusion === 'failure' ? 0xff0000 : 0xffa500,
        fields: [
          { name: "Repository", value: payload.repository.full_name, inline: true },
          { name: "Branch", value: payload.check_suite.head_branch, inline: true },
          { name: "Status", value: payload.check_suite.status, inline: true }
        ],
        timestamp: new Date().toISOString()
      };
      break;
      
    default:
      embed = {
        title: `🐙 GitHub Event: ${event}`,
        description: `Received ${event} event`,
        color: 0x6a737d,
        timestamp: new Date().toISOString()
      };
  }

  await postToDiscordChannel(channelId, embed);
  res.json({ ok: true, event, action: payload.action });
});

// Error handler
app.use((error, req, res, next) => {
  console.error("💥 Gateway error:", error);
  res.status(500).json({ error: "Internal server error" });
});

app.listen(port, () => {
  console.log(`🌐 Event gateway listening on http://localhost:${port}`);
  console.log(`📋 Configured endpoints: ${baseCfg.endpoints.map(e => e.path).join(", ")}`);
  console.log(`🔐 HMAC verification: ${hmacKey ? "enabled" : "disabled"}`);
});