import fs from "fs";
import yaml from "js-yaml";
import { logger } from "./logger.js";

type C = {
  discord: { bot: { token_secret_env: string, app_id?: string }, channels: { prs: string, deployments: string, alerts: string } };
  control_api: { base_url: string, bearer_env: string };
  event_gateway: { port: number };
};

export function loadConfig(): C {
  try {
    const doc: any = yaml.load(fs.readFileSync("discovery.yml", "utf8"));
    logger.debug("Configuration loaded successfully");
    return doc;
  } catch (error: any) {
    logger.error("Failed to load configuration", { error: error.message });
    throw error;
  }
}

export const env = (k: string, req = true) => {
  const v = process.env[k];
  if (!v && req) {
    logger.error("Missing required environment variable", { variable: k });
    throw new Error(`Missing env ${k}`);
  }
  return v || "";
};