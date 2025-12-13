import { Request, Response, NextFunction } from "express";
import { sessions, getUserById } from "../store.js";

// Extend Express Request to include user
declare global {
  namespace Express {
    interface Request {
      user?: {
        id: string;
        email: string;
        name: string;
      };
    }
  }
}

/**
 * Authentication middleware
 * Verifies session token and attaches user to request
 */
export function requireAuth(req: Request, res: Response, next: NextFunction) {
  try {
    const token = req.headers.authorization?.replace('Bearer ', '');
    
    if (!token) {
      return res.status(401).json({
        success: false,
        message: 'Authentication required'
      });
    }

    const session = sessions.get(token);
    
    if (!session) {
      return res.status(401).json({
        success: false,
        message: 'Invalid authentication token'
      });
    }

    // Check if session expired
    if (new Date() > session.expiresAt) {
      sessions.delete(token);
      return res.status(401).json({
        success: false,
        message: 'Authentication token expired'
      });
    }

    // Fetch user from store
    const user = getUserById(session.userId);
    
    if (!user) {
      return res.status(401).json({
        success: false,
        message: 'User not found'
      });
    }

    req.user = {
      id: user.id,
      email: user.email,
      name: user.name
    };

    next();
  } catch (error) {
    console.error('Auth middleware error:', error);
    return res.status(500).json({
      success: false,
      message: 'Authentication error'
    });
  }
}

/**
 * Optional authentication middleware
 * Attaches user to request if token is valid, but doesn't require it
 */
export function optionalAuth(req: Request, res: Response, next: NextFunction) {
  try {
    const token = req.headers.authorization?.replace('Bearer ', '');
    
    if (!token) {
      return next();
    }

    const session = sessions.get(token);
    
    if (!session || new Date() > session.expiresAt) {
      return next();
    }

    const user = getUserById(session.userId);
    
    if (!user) {
      return next();
    }

    req.user = {
      id: user.id,
      email: user.email,
      name: user.name
    };

    next();
  } catch (error) {
    console.error('Optional auth middleware error:', error);
    next();
  }
}
