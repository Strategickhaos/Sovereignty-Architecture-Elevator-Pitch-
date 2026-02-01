import { REST, Routes, SlashCommandBuilder, ChatInputCommandInteraction, EmbedBuilder, SlashCommandStringOption, SlashCommandIntegerOption } from "discord.js";

export async function registerCommands(token: string, appId: string) {
  const cmds = [
    new SlashCommandBuilder().setName("status").setDescription("Service status")
      .addStringOption((o: SlashCommandStringOption) => o.setName("service").setRequired(true)),
    new SlashCommandBuilder().setName("logs").setDescription("Tail logs")
      .addStringOption((o: SlashCommandStringOption) => o.setName("service").setRequired(true))
      .addIntegerOption((o: SlashCommandIntegerOption) => o.setName("tail").setRequired(false)),
    new SlashCommandBuilder().setName("deploy").setDescription("Deploy tag to env")
      .addStringOption((o: SlashCommandStringOption) => o.setName("env").setRequired(true).addChoices(
        { name: "dev", value: "dev" }, { name: "staging", value: "staging" }, { name: "prod", value: "prod" }))
      .addStringOption((o: SlashCommandStringOption) => o.setName("tag").setRequired(true)),
    new SlashCommandBuilder().setName("scale").setDescription("Scale service")
      .addStringOption((o: SlashCommandStringOption) => o.setName("service").setRequired(true))
      .addIntegerOption((o: SlashCommandIntegerOption) => o.setName("replicas").setRequired(true))
  ].map(c => c.toJSON());

  const rest = new REST({ version: "10" }).setToken(token);
  await rest.put(Routes.applicationCommands(appId), { body: cmds });
}

export function embed(title: string, description: string) {
  return new EmbedBuilder().setTitle(title).setDescription(description).setColor(0x2f81f7).toJSON();
}