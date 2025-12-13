import { z } from "zod";
import { randomUUID } from "crypto";

export const UserSchema = z.object({
  id: z.string(),
  username: z.string().min(3).max(32),
  discordId: z.string(),
  email: z.string().email().optional(),
  roles: z.array(z.string()).default([]),
  createdAt: z.string(),
  updatedAt: z.string()
});

export type User = z.infer<typeof UserSchema>;

export class UserStore {
  private users: Map<string, User> = new Map();
  private usersByDiscordId: Map<string, User> = new Map();

  register(username: string, discordId: string, email?: string): User {
    // Check if user already exists
    const existing = this.usersByDiscordId.get(discordId);
    if (existing) {
      throw new Error("User already registered");
    }

    const user: User = {
      id: randomUUID(),
      username,
      discordId,
      email,
      roles: [],
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };

    this.users.set(user.id, user);
    this.usersByDiscordId.set(user.discordId, user);
    return user;
  }

  findByDiscordId(discordId: string): User | undefined {
    return this.usersByDiscordId.get(discordId);
  }

  findById(id: string): User | undefined {
    return this.users.get(id);
  }

  list(): User[] {
    return Array.from(this.users.values());
  }

  updateRoles(id: string, roles: string[]): User {
    const user = this.users.get(id);
    if (!user) {
      throw new Error("User not found");
    }
    user.roles = roles;
    user.updatedAt = new Date().toISOString();
    return user;
  }
}

export const userStore = new UserStore();
