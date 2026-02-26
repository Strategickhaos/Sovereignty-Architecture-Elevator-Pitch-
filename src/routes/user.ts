import type { Request, Response } from "express";
import { userStore } from "../models/user.js";
import { z } from "zod";

const RegisterSchema = z.object({
  username: z.string().min(3).max(32),
  discordId: z.string(),
  email: z.string().email().optional()
});

export function userRoutes() {
  return {
    register: async (req: Request, res: Response) => {
      try {
        const data = RegisterSchema.parse(req.body);
        const user = userStore.register(data.username, data.discordId, data.email);
        res.status(201).json({ success: true, user });
      } catch (err: any) {
        if (err.message === "User already registered") {
          res.status(409).json({ success: false, error: err.message });
        } else if (err.name === "ZodError") {
          res.status(400).json({ success: false, error: "Invalid input", details: err.errors });
        } else {
          res.status(500).json({ success: false, error: "Internal server error" });
        }
      }
    },
    
    getUser: async (req: Request, res: Response) => {
      try {
        const { discordId } = req.params;
        const user = userStore.findByDiscordId(discordId);
        if (!user) {
          res.status(404).json({ success: false, error: "User not found" });
        } else {
          res.json({ success: true, user });
        }
      } catch (err: any) {
        res.status(500).json({ success: false, error: "Internal server error" });
      }
    },

    listUsers: async (req: Request, res: Response) => {
      try {
        const users = userStore.list();
        res.json({ success: true, users, count: users.length });
      } catch (err: any) {
        res.status(500).json({ success: false, error: "Internal server error" });
      }
    }
  };
}
