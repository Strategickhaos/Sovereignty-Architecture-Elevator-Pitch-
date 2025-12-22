/**
 * StrategicKhaos CTF Brain - Discord Bot Integration
 * Add CTF methodology commands to Discord bot
 */

import { SlashCommandBuilder, EmbedBuilder, ChatInputCommandInteraction } from "discord.js";
import { CTFBrain } from './ctf-brain/index.js';

const brain = new CTFBrain();

/**
 * Get CTF Brain slash commands
 */
export function getCTFBrainCommands() {
  return [
    new SlashCommandBuilder()
      .setName("ctf-query")
      .setDescription("Find pentest methodology based on keywords")
      .addStringOption(o => o
        .setName("keywords")
        .setDescription("Search keywords (e.g., 'web sql injection')")
        .setRequired(true)
      ),
    
    new SlashCommandBuilder()
      .setName("ctf-tool")
      .setDescription("Find methodology nodes that use a specific tool")
      .addStringOption(o => o
        .setName("toolname")
        .setDescription("Tool name (e.g., 'nmap', 'metasploit')")
        .setRequired(true)
      ),
    
    new SlashCommandBuilder()
      .setName("ctf-node")
      .setDescription("Get details about a specific methodology node")
      .addStringOption(o => o
        .setName("node-id")
        .setDescription("Node ID (e.g., '01-Ua-Recon')")
        .setRequired(true)
      ),
    
    new SlashCommandBuilder()
      .setName("ctf-next")
      .setDescription("Get recommended next steps from a node")
      .addStringOption(o => o
        .setName("node-id")
        .setDescription("Current node ID")
        .setRequired(true)
      ),
    
    new SlashCommandBuilder()
      .setName("ctf-path")
      .setDescription("Find workflow path between two nodes")
      .addStringOption(o => o
        .setName("start")
        .setDescription("Start node ID")
        .setRequired(true)
      )
      .addStringOption(o => o
        .setName("end")
        .setDescription("End node ID")
        .setRequired(true)
      ),
    
    new SlashCommandBuilder()
      .setName("ctf-list")
      .setDescription("List all CTF Brain methodology nodes"),
    
    new SlashCommandBuilder()
      .setName("ctf-info")
      .setDescription("Show CTF Brain metadata and philosophy")
  ];
}

/**
 * Handle CTF Brain command interactions
 */
export async function handleCTFBrainCommand(interaction: ChatInputCommandInteraction) {
  const commandName = interaction.commandName;

  try {
    switch (commandName) {
      case "ctf-query":
        await handleQueryCommand(interaction);
        break;
      case "ctf-tool":
        await handleToolCommand(interaction);
        break;
      case "ctf-node":
        await handleNodeCommand(interaction);
        break;
      case "ctf-next":
        await handleNextCommand(interaction);
        break;
      case "ctf-path":
        await handlePathCommand(interaction);
        break;
      case "ctf-list":
        await handleListCommand(interaction);
        break;
      case "ctf-info":
        await handleInfoCommand(interaction);
        break;
      default:
        await interaction.reply({ content: "Unknown CTF Brain command", ephemeral: true });
    }
  } catch (error: any) {
    console.error('CTF Brain command error:', error);
    await interaction.reply({ content: `Error: ${error.message}`, ephemeral: true });
  }
}

async function handleQueryCommand(interaction: ChatInputCommandInteraction) {
  const query = interaction.options.getString("keywords", true);
  const results = brain.findNodesByTrigger(query);

  if (results.length === 0) {
    await interaction.reply({ content: `No methodology nodes found for: "${query}"`, ephemeral: true });
    return;
  }

  const embed = new EmbedBuilder()
    .setTitle(`🔍 CTF Brain Query: "${query}"`)
    .setColor(0x00ff00)
    .setDescription(`Found ${results.length} matching node(s)`)
    .setTimestamp();

  results.slice(0, 5).forEach((result, index) => {
    embed.addFields({
      name: `${index + 1}. ${result.nodeId}: ${result.node.name}`,
      value: `**Score:** ${result.score}\n**PLL:** ${result.node.pll_analog}\n**Description:** ${result.node.description}\n**Triggers:** ${result.matchedTriggers.join(', ')}`,
      inline: false
    });
  });

  if (results.length > 5) {
    embed.setFooter({ text: `Showing top 5 of ${results.length} results` });
  }

  await interaction.reply({ embeds: [embed] });
}

async function handleToolCommand(interaction: ChatInputCommandInteraction) {
  const toolName = interaction.options.getString("toolname", true);
  const results = brain.findNodesByTool(toolName);

  if (results.length === 0) {
    await interaction.reply({ content: `No nodes found using tool: "${toolName}"`, ephemeral: true });
    return;
  }

  const embed = new EmbedBuilder()
    .setTitle(`🔧 Tool Search: "${toolName}"`)
    .setColor(0x00aaff)
    .setDescription(`Found ${results.length} node(s) using this tool`)
    .setTimestamp();

  results.forEach((result, index) => {
    embed.addFields({
      name: `${index + 1}. ${result.nodeId}: ${result.node.name}`,
      value: `**Tools:** ${result.node.tools.join(', ')}\n**Description:** ${result.node.description}`,
      inline: false
    });
  });

  await interaction.reply({ embeds: [embed] });
}

async function handleNodeCommand(interaction: ChatInputCommandInteraction) {
  const nodeId = interaction.options.getString("node-id", true);
  const node = brain.getNode(nodeId);

  if (!node) {
    await interaction.reply({ content: `Node not found: "${nodeId}"`, ephemeral: true });
    return;
  }

  const embed = new EmbedBuilder()
    .setTitle(`${nodeId}: ${node.name}`)
    .setColor(0xff9900)
    .setDescription(node.description)
    .addFields(
      { name: '🧩 PLL Algorithm', value: node.pll_analog, inline: false },
      { name: '🛠️ Tools', value: node.tools.join(', '), inline: false },
      { name: '🎯 Triggers', value: node.triggers.join(', '), inline: false },
      { name: '📊 Expected Output', value: node.expected_output.join(', '), inline: false }
    )
    .setTimestamp();

  const nextNodes = brain.getNextNodes(nodeId);
  if (nextNodes.length > 0) {
    const nextSteps = nextNodes.map(id => {
      const n = brain.getNode(id);
      return `• ${id}: ${n?.name}`;
    }).join('\n');
    embed.addFields({ name: '➡️ Next Steps', value: nextSteps, inline: false });
  }

  await interaction.reply({ embeds: [embed] });
}

async function handleNextCommand(interaction: ChatInputCommandInteraction) {
  const nodeId = interaction.options.getString("node-id", true);
  const node = brain.getNode(nodeId);

  if (!node) {
    await interaction.reply({ content: `Node not found: "${nodeId}"`, ephemeral: true });
    return;
  }

  const workflows = brain.getRecommendedWorkflow(nodeId);

  if (workflows.length === 0) {
    await interaction.reply({ content: `No next steps available from ${nodeId}: ${node.name}`, ephemeral: true });
    return;
  }

  const embed = new EmbedBuilder()
    .setTitle(`➡️ Next Steps from ${nodeId}: ${node.name}`)
    .setColor(0x9900ff)
    .setDescription(`${workflows.length} recommended workflow(s)`)
    .setTimestamp();

  workflows.forEach((workflow, index) => {
    embed.addFields({
      name: `${index + 1}. ${workflow.description}`,
      value: '\u200B',
      inline: false
    });
  });

  await interaction.reply({ embeds: [embed] });
}

async function handlePathCommand(interaction: ChatInputCommandInteraction) {
  const start = interaction.options.getString("start", true);
  const end = interaction.options.getString("end", true);
  
  const path = brain.findPath(start, end);

  if (!path) {
    await interaction.reply({ content: `No path found from ${start} to ${end}`, ephemeral: true });
    return;
  }

  const embed = new EmbedBuilder()
    .setTitle(`🗺️ Workflow Path: ${start} → ${end}`)
    .setColor(0xff00ff)
    .setDescription(path.description)
    .setTimestamp();

  const details = path.path.map((nodeId, index) => {
    const node = brain.getNode(nodeId);
    return `**${index + 1}. ${nodeId}: ${node?.name}**\n${node?.description}\nPLL: ${node?.pll_analog}`;
  }).join('\n\n');

  embed.addFields({ name: 'Detailed Steps', value: details, inline: false });

  await interaction.reply({ embeds: [embed] });
}

async function handleListCommand(interaction: ChatInputCommandInteraction) {
  const nodes = brain.getAllNodes();
  const nodeList = Object.entries(nodes).map(([nodeId, node]) => {
    return `**${nodeId}**: ${node.name} - ${node.description}`;
  }).join('\n\n');

  const embed = new EmbedBuilder()
    .setTitle('📋 All CTF Brain Methodology Nodes')
    .setColor(0x00ffff)
    .setDescription(nodeList)
    .setTimestamp();

  await interaction.reply({ embeds: [embed] });
}

async function handleInfoCommand(interaction: ChatInputCommandInteraction) {
  const metadata = brain.getMetadata();
  const weights = brain.getQuadrantWeights();
  const nodeCount = Object.keys(brain.getAllNodes()).length;
  const edgeCount = brain.getEdges().length;

  const embed = new EmbedBuilder()
    .setTitle(`${metadata.name} v${metadata.version}`)
    .setColor(0xffaa00)
    .setDescription(metadata.description)
    .addFields(
      { name: '👤 Author', value: metadata.author, inline: false },
      { name: '🧠 Philosophy', value: metadata.philosophy, inline: false },
      { name: '📊 Statistics', value: `Nodes: ${nodeCount} | Edges: ${edgeCount}`, inline: false },
      { name: '⚖️ Quadrant Weights', value: 
        `Tool Ready: ${weights.tool_ready}\n` +
        `Context Match: ${weights.context_match}\n` +
        `Success Rate: ${weights.success_rate}\n` +
        `Efficiency: ${weights.efficiency}`, 
        inline: false 
      }
    )
    .setTimestamp();

  await interaction.reply({ embeds: [embed] });
}
