import { Client, GatewayIntentBits, Interaction } from "discord.js";
import { registerCommands, embed } from "./discord.js";
import { env, loadConfig } from "./config.js";

const cfg = loadConfig();
const token = env("DISCORD_TOKEN");
const appId = env("APP_ID", false) || cfg.discord?.bot?.app_id || "";

const client = new Client({ intents: [GatewayIntentBits.Guilds] });

client.once("ready", async () => {
  await registerCommands(token, appId);
  console.log("Bot ready");
});

client.on("interactionCreate", async (i: Interaction) => {
  if (!i.isChatInputCommand()) return;
  try {
    if (i.commandName === "status") {
      const svc = i.options.getString("service", true);
      const r = await fetch(`${cfg.control_api.base_url}/status/${svc}`, {
        headers: { Authorization: `Bearer ${env(cfg.control_api.bearer_env)}` }
      }).then(r => r.json());
      await i.reply({ embeds: [embed(`Status: ${svc}`, `state: ${r.state}\nversion: ${r.version}`)] });
    } else if (i.commandName === "logs") {
      const svc = i.options.getString("service", true);
      const tail = i.options.getInteger("tail") || 200;
      const r = await fetch(`${cfg.control_api.base_url}/logs/${svc}?tail=${tail}`, {
        headers: { Authorization: `Bearer ${env(cfg.control_api.bearer_env)}` }
      }).then(r => r.text());
      await i.reply({ content: "```\n" + r.slice(0, 1800) + "\n```" });
    } else if (i.commandName === "deploy") {
      const envName = i.options.getString("env", true);
      const tag = i.options.getString("tag", true);
      const r = await fetch(`${cfg.control_api.base_url}/deploy`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${env(cfg.control_api.bearer_env)}` },
        body: JSON.stringify({ env: envName, tag })
      }).then(r => r.json());
      await i.reply({ embeds: [embed("Deploy", `env: ${envName}\ntag: ${tag}\nresult: ${r.status}`)] });
    } else if (i.commandName === "scale") {
      const svc = i.options.getString("service", true);
      const replicas = i.options.getInteger("replicas", true);
      const r = await fetch(`${cfg.control_api.base_url}/scale`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${env(cfg.control_api.bearer_env)}` },
        body: JSON.stringify({ service: svc, replicas })
      }).then(r => r.json());
      await i.reply({ embeds: [embed("Scale", `service: ${svc}\nreplicas: ${replicas}\nresult: ${r.status}`)] });
    } else if (i.commandName === "request") {
      const project = i.options.getString("project", true);
      const description = i.options.getString("description", true);
      const expertsStr = i.options.getString("experts", false);
      const experts = expertsStr ? expertsStr.split(",").map(e => e.trim()) : null;
      
      const refinoryPort = cfg.refinory?.ports?.api || 8085;
      const r = await fetch(`http://localhost:${refinoryPort}/requests`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          project, 
          description, 
          requester: i.user.username,
          experts 
        })
      }).then(r => r.json());
      
      const expertsInfo = experts ? `\nExperts: ${experts.join(", ")}` : "";
      await i.reply({ 
        embeds: [embed(
          "🧠 Refinory Request Created", 
          `**Project:** ${project}\n**Request ID:** ${r.request_id}\n**Status:** ${r.status}${expertsInfo}\n\n${r.message}`
        )] 
      });
    } else if (i.commandName === "refinory-status") {
      const requestId = i.options.getString("request_id", true);
      
      const refinoryPort = cfg.refinory?.ports?.api || 8085;
      const r = await fetch(`http://localhost:${refinoryPort}/requests/${requestId}`).then(r => r.json());
      
      const progressBar = "█".repeat(Math.floor(r.progress / 10)) + "░".repeat(10 - Math.floor(r.progress / 10));
      const activeExperts = r.active_experts && r.active_experts.length > 0 
        ? `\n**Active Experts:** ${r.active_experts.join(", ")}` 
        : "";
      const artifacts = r.artifacts && r.artifacts.length > 0
        ? `\n**Artifacts:** ${r.artifacts.length} files generated`
        : "";
      
      await i.reply({ 
        embeds: [embed(
          `📊 Refinory Status: ${r.project}`,
          `**Request ID:** ${requestId}\n**Status:** ${r.status}\n**Progress:** ${progressBar} ${r.progress}%${activeExperts}${artifacts}\n**Updated:** ${new Date(r.updated_at).toLocaleString()}`
        )]
      });
    }
  } catch (e: any) {
    await i.reply({ content: `Error: ${e.message}` });
  }
});

client.login(token);