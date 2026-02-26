import express from "express";
import bodyParser from "body-parser";
import path from "path";
import { fileURLToPath } from "url";
import { REST } from "discord.js";
import { loadConfig, env } from "./config.js";
import { githubRoutes } from "./routes/github.js";
import { authRoutes } from "./routes/auth.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const cfg = loadConfig();
const app = express();

// Serve static files from public directory
app.use(express.static(path.join(__dirname, '../public')));

// keep raw for signature
app.use(bodyParser.json({
  verify: (req: any, _res, buf) => { req.rawBody = buf.toString(); }
}));

const rest = new REST({ version: "10" }).setToken(env("DISCORD_TOKEN"));

const channelIds = {
  prs: process.env.PRS_CHANNEL_ID!,
  deployments: process.env.DEPLOYMENTS_CHANNEL_ID!,
  alerts: process.env.ALERTS_CHANNEL_ID!
};

// Authentication routes
app.use("/api/auth", authRoutes);

// GitHub webhook routes
app.post("/webhooks/github", githubRoutes(rest, channelIds, env("GITHUB_WEBHOOK_SECRET")));

// Serve login page at root
app.get("/", (_req, res) => {
  res.sendFile(path.join(__dirname, '../public/login.html'));
});

app.get("/login", (_req, res) => {
  res.sendFile(path.join(__dirname, '../public/login.html'));
});

app.get("/dashboard", (_req, res) => {
  res.sendFile(path.join(__dirname, '../public/dashboard.html'));
});

const port = Number(process.env.PORT || cfg.event_gateway.port || 3001);
app.listen(port, () => console.log(`Event gateway on :${port}`));