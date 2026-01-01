import { REST, Routes, SlashCommandBuilder, EmbedBuilder } from "discord.js";
export async function registerCommands(token, appId) {
    const cmds = [
        new SlashCommandBuilder().setName("status").setDescription("Service status")
            .addStringOption(o => o.setName("service").setRequired(true)),
        new SlashCommandBuilder().setName("logs").setDescription("Tail logs")
            .addStringOption(o => o.setName("service").setRequired(true))
            .addIntegerOption(o => o.setName("tail").setRequired(false)),
        new SlashCommandBuilder().setName("deploy").setDescription("Deploy tag to env")
            .addStringOption(o => o.setName("env").setRequired(true).addChoices({ name: "dev", value: "dev" }, { name: "staging", value: "staging" }, { name: "prod", value: "prod" }))
            .addStringOption(o => o.setName("tag").setRequired(true)),
        new SlashCommandBuilder().setName("scale").setDescription("Scale service")
            .addStringOption(o => o.setName("service").setRequired(true))
            .addIntegerOption(o => o.setName("replicas").setRequired(true)),
        new SlashCommandBuilder().setName("request").setDescription("Create Refinory architecture request")
            .addStringOption(o => o.setName("project").setDescription("Project name").setRequired(true))
            .addStringOption(o => o.setName("description").setDescription("Project description").setRequired(true))
            .addStringOption(o => o.setName("experts").setDescription("Comma-separated expert names (optional)").setRequired(false)),
        new SlashCommandBuilder().setName("refinory-status").setDescription("Get Refinory request status")
            .addStringOption(o => o.setName("request_id").setDescription("Request ID").setRequired(true))
    ].map(c => c.toJSON());
    const rest = new REST({ version: "10" }).setToken(token);
    await rest.put(Routes.applicationCommands(appId), { body: cmds });
}
export function embed(title, description) {
    return new EmbedBuilder().setTitle(title).setDescription(description).setColor(0x2f81f7).toJSON();
}
