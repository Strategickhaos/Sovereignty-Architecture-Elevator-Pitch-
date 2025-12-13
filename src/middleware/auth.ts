import { Request, Response, NextFunction } from "express";

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

// Temporary session store (should match the one in auth.ts)
// In production, use a shared store like Redis
const sessions = new Map<string, {
  userId: string;
  createdAt: Date;
  expiresAt: Date;
}>();

/**
 * Authentication middleware
 * Verifies JWT token and attaches user to request
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

    // In production, fetch user from database
    // For now, we'll attach minimal user info
    req.user = {
      id: session.userId,
      email: '', // Would fetch from database
      name: ''   // Would fetch from database
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

    req.user = {
      id: session.userId,
      email: '',
      name: ''
    };

    next();
  } catch (error) {
    console.error('Optional auth middleware error:', error);
    next();
  }
}
