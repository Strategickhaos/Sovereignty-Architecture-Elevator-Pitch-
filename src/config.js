// src/config.js
import fs from "fs";
import path from "path";
import yaml from "js-yaml";
import { fileURLToPath } from "url";
import dotenv from "dotenv";

dotenv.config(); // loads .env if present

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const discoveryPath =
  process.env.DISCOVERY_CONFIG_PATH ||
  path.join(__dirname, "..", "discovery.yml");

export function loadConfig() {
  const raw = fs.readFileSync(discoveryPath, "utf8");
  const cfg = yaml.load(raw);

  return cfg;
}

export function getChannelId(channelName) {
  const channels = {
    "#cluster-status": process.env.CH_CLUSTER_STATUS_ID,
    "#alerts": process.env.CH_ALERTS_ID,
    "#deployments": process.env.CH_DEPLOYMENTS_ID,
    "#prs": process.env.CH_PRS_ID,
    "#agents": process.env.CH_AGENTS_ID,
    "#inference-stream": process.env.CH_INFERENCE_ID,
    "#dev-feed": process.env.CH_DEV_FEED_ID
  };
  
  return channels[channelName] || null;
}

export function validateConfig() {
  const cfg = loadConfig();
  const required = [
    'org.name',
    'discord.guild_id',
    'discord.bot.app_id',
    'git.org'
  ];
  
  const missing = required.filter(path => {
    const keys = path.split('.');
    let obj = cfg;
    for (const key of keys) {
      if (!obj || obj[key] === null || obj[key] === '') {
        return true;
      }
      obj = obj[key];
    }
    return false;
  });
  
  if (missing.length > 0) {
    throw new Error(`Missing required config: ${missing.join(', ')}`);
  }
  
  return cfg;
}