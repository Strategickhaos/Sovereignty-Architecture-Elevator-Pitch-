/**
 * Shared data store for users and sessions
 * In production, replace with database and Redis
 */

import * as crypto from "crypto";

// User type
export interface User {
  id: string;
  email: string;
  passwordHash: string;
  name: string;
  createdAt: Date;
}

// Session type
export interface Session {
  userId: string;
  createdAt: Date;
  expiresAt: Date;
}

// In-memory stores (replace with database/Redis in production)
export const users = new Map<string, User>();
export const usersByEmail = new Map<string, User>();
export const sessions = new Map<string, Session>();

// Helper function to add a user
export function addUser(email: string, user: User): void {
  users.set(user.id, user);
  usersByEmail.set(email.toLowerCase(), user);
}

// Helper function to get user by email
export function getUserByEmail(email: string): User | undefined {
  return usersByEmail.get(email.toLowerCase());
}

// Helper function to get user by ID
export function getUserById(userId: string): User | undefined {
  return users.get(userId);
}

// Helper function to hash passwords
export function hashPassword(password: string, salt?: string): { hash: string; salt: string } {
  const passwordSalt = salt || crypto.randomBytes(16).toString('hex');
  const hash = crypto.pbkdf2Sync(password, passwordSalt, 10000, 64, 'sha512').toString('hex');
  return { hash, salt: passwordSalt };
}

// Helper function to verify password
export function verifyPassword(password: string, hash: string, salt: string): boolean {
  const { hash: computedHash } = hashPassword(password, salt);
  return computedHash === hash;
}

// Helper function to generate auth token
export function generateAuthToken(): string {
  return crypto.randomBytes(32).toString('hex');
}

// Initialize with a demo user
const demoPasswordData = hashPassword('demo123');
const demoUser: User = {
  id: 'demo-user-id',
  email: 'demo@example.com',
  passwordHash: demoPasswordData.hash + ':' + demoPasswordData.salt,
  name: 'Demo User',
  createdAt: new Date()
};
addUser('demo@example.com', demoUser);
