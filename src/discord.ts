import { REST, Routes, SlashCommandBuilder, ChatInputCommandInteraction, EmbedBuilder } from "discord.js";

export async function registerCommands(token: string, appId: string) {
  const cmds = [
    new SlashCommandBuilder().setName("status").setDescription("Service status")
      .addStringOption(o => o.setName("service").setRequired(true)),
    new SlashCommandBuilder().setName("logs").setDescription("Tail logs")
      .addStringOption(o => o.setName("service").setRequired(true))
      .addIntegerOption(o => o.setName("tail").setRequired(false)),
    new SlashCommandBuilder().setName("deploy").setDescription("Deploy tag to env")
      .addStringOption(o => o.setName("env").setRequired(true).addChoices(
        { name: "dev", value: "dev" }, { name: "staging", value: "staging" }, { name: "prod", value: "prod" }))
      .addStringOption(o => o.setName("tag").setRequired(true)),
    new SlashCommandBuilder().setName("scale").setDescription("Scale service")
      .addStringOption(o => o.setName("service").setRequired(true))
      .addIntegerOption(o => o.setName("replicas").setRequired(true)),
    new SlashCommandBuilder().setName("profile").setDescription("View user profile information")
      .addUserOption(o => o.setName("user").setDescription("User to view profile for").setRequired(false))
  ].map(c => c.toJSON());

  const rest = new REST({ version: "10" }).setToken(token);
  await rest.put(Routes.applicationCommands(appId), { body: cmds });
}

export function embed(title: string, description: string) {
  return new EmbedBuilder().setTitle(title).setDescription(description).setColor(0x2f81f7).toJSON();
}

export function createProfileEmbed(user: any, member: any) {
  const embed = new EmbedBuilder()
    .setTitle(`Profile: ${user.username}`)
    .setColor(0x2f81f7)
    .setThumbnail(user.displayAvatarURL({ size: 256 }))
    .addFields(
      { name: "Username", value: user.username, inline: true },
      { name: "User ID", value: user.id, inline: true },
      { name: "Account Created", value: `<t:${Math.floor(user.createdTimestamp / 1000)}:R>`, inline: true }
    );

  if (member) {
    embed.addFields(
      { name: "Joined Server", value: `<t:${Math.floor(member.joinedTimestamp / 1000)}:R>`, inline: true },
      { name: "Roles", value: member.roles.cache.size > 1 ? member.roles.cache.filter((r: any) => r.id !== member.guild.id).map((r: any) => r.name).join(", ") : "None", inline: false }
    );

    if (member.nickname) {
      embed.addFields({ name: "Nickname", value: member.nickname, inline: true });
    }
  }

  return embed;
}