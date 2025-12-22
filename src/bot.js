// src/bot.js
import { 
  Client, 
  GatewayIntentBits, 
  REST, 
  Routes, 
  SlashCommandBuilder,
  EmbedBuilder 
} from "discord.js";
import { loadConfig, getChannelId } from "./config.js";
import { RefinoryClient } from "./refinory/client.js";
import { FeedbackStore } from "./feedback/store.js";

const config = loadConfig();
const feedbackStore = new FeedbackStore();
const token = process.env.DISCORD_TOKEN;
const guildId = config.discord.guild_id;
const appId = config.discord.bot.app_id;

if (!token) {
  console.error("❌ DISCORD_TOKEN not set");
  process.exit(1);
}
if (!guildId || !appId) {
  console.error("❌ discord.guild_id or discord.bot.app_id missing in discovery.yml");
  process.exit(1);
}

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds, 
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent
  ],
});

const refinory = new RefinoryClient();

// Build commands from discovery.yml.commands.list
const commandsFromCfg = (config.commands?.list || []).map((cmd) => {
  let builder = new SlashCommandBuilder()
    .setName(cmd.name)
    .setDescription(cmd.description || "command");

  (cmd.params || []).forEach((p) => {
    if (p.type === "string") {
      builder.addStringOption((o) => {
        o.setName(p.name).setDescription(`${p.name} parameter`);
        if (p.required) o.setRequired(true);
        if (p.enum) o.addChoices(...p.enum.map((e) => ({ name: e, value: e })));
        return o;
      });
    }

    if (p.type === "int") {
      builder.addIntegerOption((o) => {
        o.setName(p.name).setDescription(`${p.name} parameter`);
        if (p.required) o.setRequired(true);
        return o;
      });
    }
  });

  return builder.toJSON();
});

// Register slash commands on startup
async function registerCommands() {
  const rest = new REST({ version: "10" }).setToken(token);
  await rest.put(Routes.applicationGuildCommands(appId, guildId), {
    body: commandsFromCfg,
  });
  console.log(`✅ Registered ${commandsFromCfg.length} commands for guild ${guildId}`);
}

client.once("ready", () => {
  console.log(`🤖 Logged in as ${client.user.tag}`);
  console.log(`🎯 Serving guild: ${guildId}`);
  console.log(`🔧 Environment: ${config.testing?.dry_run ? 'DRY-RUN' : 'LIVE'}`);
});

client.on("interactionCreate", async (interaction) => {
  if (!interaction.isChatInputCommand()) return;

  const name = interaction.commandName;
  const dryRun = config.testing?.dry_run ?? true;

  try {
    await interaction.deferReply();

    switch (name) {
      case "status": {
        const svc = interaction.options.getString("service");
        const embed = new EmbedBuilder()
          .setTitle(`📊 Service Status: ${svc}`)
          .setDescription(dryRun ? 
            `\`DRY-RUN\` Would check status for **${svc}**\n\nNext: Integrate with control_api at ${config.infra.control_api.base_url}` :
            `Checking status for **${svc}**...`
          )
          .setColor(dryRun ? 0xffa500 : 0x00ff00)
          .addFields([
            { name: "Service", value: svc, inline: true },
            { name: "Environment", value: "dev", inline: true },
            { name: "Status", value: dryRun ? "DRY-RUN" : "UNKNOWN", inline: true }
          ])
          .setTimestamp();
        
        await interaction.editReply({ embeds: [embed] });
        break;
      }

      case "logs": {
        const svc = interaction.options.getString("service");
        const tail = interaction.options.getInteger("tail") ?? 200;
        
        const embed = new EmbedBuilder()
          .setTitle(`📄 Service Logs: ${svc}`)
          .setDescription(dryRun ? 
            `\`DRY-RUN\` Would tail last ${tail} lines for **${svc}**` :
            `Fetching last ${tail} lines for **${svc}**...`
          )
          .setColor(0x0099ff)
          .setTimestamp();
        
        await interaction.editReply({ embeds: [embed] });
        break;
      }

      case "deploy": {
        const env = interaction.options.getString("env");
        const tag = interaction.options.getString("tag");
        
        const embed = new EmbedBuilder()
          .setTitle("🚀 Deployment Request")
          .setDescription(dryRun ? 
            `\`DRY-RUN\` Would deploy **${tag}** to **${env}**` :
            `Deploying **${tag}** to **${env}**...`
          )
          .setColor(env === 'prod' ? 0xff0000 : 0x00ff00)
          .addFields([
            { name: "Tag", value: tag, inline: true },
            { name: "Environment", value: env, inline: true },
            { name: "Requester", value: interaction.user.tag, inline: true }
          ])
          .setTimestamp();
        
        await interaction.editReply({ embeds: [embed] });
        
        // Notify deployment channel
        const deployChannel = getChannelId(config.refinory?.discord?.announce_channel || "#deployments");
        if (deployChannel) {
          const notifyEmbed = new EmbedBuilder()
            .setTitle("🔔 Deployment Initiated")
            .setDescription(`${interaction.user} initiated deployment via Discord`)
            .addFields([
              { name: "Tag", value: tag, inline: true },
              { name: "Environment", value: env, inline: true }
            ])
            .setColor(0x0099ff)
            .setTimestamp();
            
          const channel = client.channels.cache.get(deployChannel);
          if (channel) {
            await channel.send({ embeds: [notifyEmbed] });
          }
        }
        break;
      }

      case "scale": {
        const svc = interaction.options.getString("service");
        const replicas = interaction.options.getInteger("replicas");
        
        const embed = new EmbedBuilder()
          .setTitle("⚖️ Scaling Request")
          .setDescription(dryRun ? 
            `\`DRY-RUN\` Would scale **${svc}** to **${replicas}** replicas` :
            `Scaling **${svc}** to **${replicas}** replicas...`
          )
          .setColor(0xff9900)
          .addFields([
            { name: "Service", value: svc, inline: true },
            { name: "Replicas", value: replicas.toString(), inline: true },
            { name: "Requester", value: interaction.user.tag, inline: true }
          ])
          .setTimestamp();
        
        await interaction.editReply({ embeds: [embed] });
        break;
      }

      case "request": {
        const project = interaction.options.getString("project");
        const description = interaction.options.getString("description");
        const experts = interaction.options.getString("experts");
        
        const requestId = await refinory.createRequest({
          project,
          description,
          requester: interaction.user.tag,
          experts: experts ? experts.split(',').map(e => e.trim()) : null
        });
        
        const embed = new EmbedBuilder()
          .setTitle("🧠 Refinory Request Created")
          .setDescription(`Architecture request submitted to Refinory AI experts`)
          .addFields([
            { name: "Request ID", value: requestId, inline: true },
            { name: "Project", value: project, inline: true },
            { name: "Requester", value: interaction.user.tag, inline: true },
            { name: "Description", value: description.substring(0, 1000) },
            { name: "Experts", value: experts || "Auto-selected", inline: true }
          ])
          .setColor(0x9932cc)
          .setTimestamp();
        
        await interaction.editReply({ embeds: [embed] });
        
        // Notify agents channel
        const agentsChannel = getChannelId("#agents");
        if (agentsChannel) {
          const notifyEmbed = new EmbedBuilder()
            .setTitle("🎯 New Refinory Request")
            .setDescription(`${interaction.user} submitted architecture request`)
            .addFields([
              { name: "Request ID", value: requestId, inline: true },
              { name: "Project", value: project, inline: true }
            ])
            .setColor(0x9932cc)
            .setTimestamp();
            
          const channel = client.channels.cache.get(agentsChannel);
          if (channel) {
            await channel.send({ embeds: [notifyEmbed] });
          }
        }
        break;
      }

      case "refinory-status": {
        const requestId = interaction.options.getString("request_id");
        
        const status = await refinory.getStatus(requestId);
        
        const embed = new EmbedBuilder()
          .setTitle(`🔍 Refinory Status: ${requestId}`)
          .setDescription(status.description || "Status check")
          .addFields([
            { name: "Status", value: status.status, inline: true },
            { name: "Progress", value: `${status.progress || 0}%`, inline: true },
            { name: "Experts Active", value: status.active_experts?.join(", ") || "None", inline: true }
          ])
          .setColor(status.status === 'completed' ? 0x00ff00 : 0xffa500)
          .setTimestamp();
        
        if (status.artifacts?.length) {
          embed.addFields([
            { name: "Artifacts", value: status.artifacts.slice(0, 5).join("\n") }
          ]);
        }
        
        await interaction.editReply({ embeds: [embed] });
        break;
      }

      case "feedback": {
        const command = interaction.options.getString("command");
        const rating = interaction.options.getInteger("rating");
        const comment = interaction.options.getString("comment") || "";
        
        const feedbackId = feedbackStore.submit({
          userId: interaction.user.id,
          username: interaction.user.tag,
          command,
          rating,
          comment,
          metadata: {
            guildId: interaction.guildId,
            channelId: interaction.channelId
          }
        });
        
        const embed = new EmbedBuilder()
          .setTitle("💬 Feedback Submitted")
          .setDescription("Thank you for your feedback! We appreciate your input.")
          .addFields([
            { name: "Feedback ID", value: feedbackId, inline: true },
            { name: "Command", value: command, inline: true },
            { name: "Rating", value: `${"⭐".repeat(rating)}`, inline: true },
          ])
          .setColor(0x00ff00)
          .setTimestamp();
        
        if (comment) {
          embed.addFields([
            { name: "Comment", value: comment.substring(0, 1000) }
          ]);
        }
        
        await interaction.editReply({ embeds: [embed] });
        break;
      }

      case "feedback-stats": {
        const stats = feedbackStore.getStats();
        
        const embed = new EmbedBuilder()
          .setTitle("📊 Feedback Statistics")
          .setDescription(`Analysis of user feedback across all commands`)
          .addFields([
            { name: "Total Feedback", value: stats.totalCount.toString(), inline: true },
            { name: "Average Rating", value: `${stats.averageRating} ⭐`, inline: true },
            { name: "Recent (7 days)", value: stats.recentCount.toString(), inline: true }
          ])
          .setColor(0x0099ff)
          .setTimestamp();
        
        // Rating distribution
        const ratingDist = Object.entries(stats.ratingDistribution)
          .map(([rating, count]) => `${"⭐".repeat(Number(rating))}: ${count}`)
          .join("\n");
        
        if (ratingDist) {
          embed.addFields([
            { name: "Rating Distribution", value: ratingDist, inline: true }
          ]);
        }
        
        // Command statistics
        const commandStatsStr = Object.entries(stats.commandStats)
          .slice(0, 5)
          .map(([cmd, data]) => `\`${cmd}\`: ${data.averageRating}⭐ (${data.count} reviews)`)
          .join("\n");
        
        if (commandStatsStr) {
          embed.addFields([
            { name: "Top Commands", value: commandStatsStr, inline: false }
          ]);
        }
        
        await interaction.editReply({ embeds: [embed] });
        break;
      }

      case "feedback-list": {
        const command = interaction.options.getString("command");
        const rating = interaction.options.getInteger("rating");
        
        const filters = {};
        if (command) filters.command = command;
        if (rating) filters.rating = rating;
        
        const feedbackList = feedbackStore.list(filters);
        
        if (feedbackList.length === 0) {
          await interaction.editReply("No feedback found matching your criteria.");
          break;
        }
        
        const embed = new EmbedBuilder()
          .setTitle("📝 Feedback List")
          .setDescription(`Found ${feedbackList.length} feedback entries`)
          .setColor(0x9932cc)
          .setTimestamp();
        
        // Show first 10 feedback entries
        feedbackList.slice(0, 10).forEach((fb, index) => {
          const timestamp = new Date(fb.timestamp).toLocaleDateString();
          const commentPreview = fb.comment ? fb.comment.substring(0, 100) : "No comment";
          
          embed.addFields([{
            name: `${index + 1}. ${fb.command} by ${fb.username}`,
            value: `${"⭐".repeat(fb.rating)} | ${timestamp}\n${commentPreview}`,
            inline: false
          }]);
        });
        
        if (feedbackList.length > 10) {
          embed.setFooter({ text: `Showing 10 of ${feedbackList.length} entries` });
        }
        
        await interaction.editReply({ embeds: [embed] });
        break;
      }

      default:
        await interaction.editReply(`❓ Command **${name}** not implemented yet.`);
    }
  } catch (error) {
    console.error(`Error handling command ${name}:`, error);
    const errorEmbed = new EmbedBuilder()
      .setTitle("❌ Command Error")
      .setDescription(`Failed to execute **${name}**: ${error.message}`)
      .setColor(0xff0000)
      .setTimestamp();
      
    if (interaction.deferred) {
      await interaction.editReply({ embeds: [errorEmbed] });
    } else {
      await interaction.reply({ embeds: [errorEmbed], ephemeral: true });
    }
  }
});

// Enhanced error handling
client.on('error', error => {
  console.error('Discord client error:', error);
});

process.on('unhandledRejection', error => {
  console.error('Unhandled promise rejection:', error);
});

(async () => {
  try {
    await registerCommands();
    await client.login(token);
  } catch (err) {
    console.error("❌ Bot startup error:", err);
    process.exit(1);
  }
})();