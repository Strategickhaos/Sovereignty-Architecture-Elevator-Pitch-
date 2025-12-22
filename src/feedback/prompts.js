// src/feedback/prompts.js
import { ActionRowBuilder, ButtonBuilder, ButtonStyle } from "discord.js";

/**
 * Create feedback prompt buttons
 */
export function createFeedbackButtons(commandName, requestId = null) {
  const customId = requestId 
    ? `feedback:${commandName}:${requestId}`
    : `feedback:${commandName}`;
    
  const row = new ActionRowBuilder()
    .addComponents(
      new ButtonBuilder()
        .setCustomId(`${customId}:5`)
        .setLabel("⭐⭐⭐⭐⭐")
        .setStyle(ButtonStyle.Success),
      new ButtonBuilder()
        .setCustomId(`${customId}:4`)
        .setLabel("⭐⭐⭐⭐")
        .setStyle(ButtonStyle.Primary),
      new ButtonBuilder()
        .setCustomId(`${customId}:3`)
        .setLabel("⭐⭐⭐")
        .setStyle(ButtonStyle.Secondary),
      new ButtonBuilder()
        .setCustomId(`${customId}:2`)
        .setLabel("⭐⭐")
        .setStyle(ButtonStyle.Secondary),
      new ButtonBuilder()
        .setCustomId(`${customId}:1`)
        .setLabel("⭐")
        .setStyle(ButtonStyle.Danger)
    );
    
  return row;
}

/**
 * Parse feedback button interaction
 */
export function parseFeedbackButton(customId) {
  const parts = customId.split(':');
  
  // Validate format: must have at least 3 parts (feedback:command:rating)
  // or 4 parts (feedback:command:requestId:rating)
  if (parts[0] !== 'feedback' || parts.length < 3 || parts.length > 4) {
    return null;
  }
  
  return {
    command: parts[1],
    requestId: parts.length === 4 ? parts[2] : null,
    rating: parseInt(parts[parts.length - 1])
  };
}

/**
 * Check if feedback should be prompted for this command
 */
export function shouldPromptFeedback(commandName, config) {
  const feedbackConfig = config.feedback || {};
  
  // Default commands that should prompt for feedback
  const defaultPromptCommands = ['deploy', 'request', 'scale', 'refinory-status'];
  
  const promptCommands = feedbackConfig.prompt_commands || defaultPromptCommands;
  
  return promptCommands.includes(commandName);
}

export default {
  createFeedbackButtons,
  parseFeedbackButton,
  shouldPromptFeedback
};
