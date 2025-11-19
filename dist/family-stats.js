import fs from "fs";
import yaml from "js-yaml";
import { EmbedBuilder } from "discord.js";
export function loadFamilyConfig() {
    const doc = yaml.load(fs.readFileSync("family_config.yaml", "utf8"));
    return doc;
}
export function getFamilyStats() {
    const config = loadFamilyConfig();
    const { family, projects } = config;
    let output = `\n🔥 THE FAMILY — ${family.total_count.toLocaleString()}+ STRONG 🔥\n\n`;
    output += `Not votes. Not stars. FAMILY.\n\n`;
    output += `═══════════════════════════════════════\n\n`;
    projects.forEach((project) => {
        const emoji = getCategoryEmoji(project.category);
        output += `${emoji} ${project.name}\n`;
        output += `   ${project.members.toLocaleString()} family members\n`;
        output += `   ${project.description}\n\n`;
    });
    output += `═══════════════════════════════════════\n\n`;
    output += `🌍 We span every continent\n`;
    output += `🧠 We dream in neurospice\n`;
    output += `⚡ We ride into fire together\n`;
    output += `👑 We protect the bloodline\n\n`;
    output += `Last updated: ${family.last_updated}\n`;
    return output;
}
export function getFamilyEmbed() {
    const config = loadFamilyConfig();
    const { family, projects } = config;
    const embed = new EmbedBuilder()
        .setTitle(`🔥 The Family — ${family.total_count.toLocaleString()}+ Strong`)
        .setDescription(`**Not votes. Not stars. FAMILY.**\n\n${family.description}`)
        .setColor(0xFF4500) // Fire orange color
        .setTimestamp();
    // Add project fields
    projects.forEach((project) => {
        const emoji = getCategoryEmoji(project.category);
        embed.addFields({
            name: `${emoji} ${project.name}`,
            value: `**${project.members.toLocaleString()}** family members\n${project.description}`,
            inline: false
        });
    });
    // Add footer
    embed.setFooter({
        text: `🧠⚡👑❤️🐐∞ • Last updated: ${family.last_updated}`
    });
    return embed;
}
function getCategoryEmoji(category) {
    const emojiMap = {
        "tools": "🛠️",
        "framework": "🏛️",
        "legal": "🛡️",
        "daemon": "👁️",
        "community": "🌟"
    };
    return emojiMap[category] || "📦";
}
export function calculateTotalFamily() {
    const config = loadFamilyConfig();
    return config.projects.reduce((sum, project) => sum + project.members, 0);
}
export function getFamilyByProject(projectName) {
    const config = loadFamilyConfig();
    return config.projects.find(p => p.name.toLowerCase() === projectName.toLowerCase());
}
