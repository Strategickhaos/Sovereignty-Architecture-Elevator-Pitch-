import { Request, Response, Router } from "express";
import * as crypto from "crypto";

const router = Router();

// Temporary in-memory user store (replace with database in production)
const users = new Map<string, {
  id: string;
  email: string;
  passwordHash: string;
  name: string;
  createdAt: Date;
}>();

// Temporary session store (replace with Redis/database in production)
const sessions = new Map<string, {
  userId: string;
  createdAt: Date;
  expiresAt: Date;
}>();

// Helper function to hash passwords
function hashPassword(password: string, salt?: string): { hash: string; salt: string } {
  const passwordSalt = salt || crypto.randomBytes(16).toString('hex');
  const hash = crypto.pbkdf2Sync(password, passwordSalt, 10000, 64, 'sha512').toString('hex');
  return { hash, salt: passwordSalt };
}

// Helper function to verify password
function verifyPassword(password: string, hash: string, salt: string): boolean {
  const { hash: computedHash } = hashPassword(password, salt);
  return computedHash === hash;
}

// Helper function to generate auth token
function generateAuthToken(): string {
  return crypto.randomBytes(32).toString('hex');
}

// Add a demo user for testing
const demoPasswordData = hashPassword('demo123');
users.set('demo@example.com', {
  id: 'demo-user-id',
  email: 'demo@example.com',
  passwordHash: demoPasswordData.hash + ':' + demoPasswordData.salt,
  name: 'Demo User',
  createdAt: new Date()
});

/**
 * POST /api/auth/login
 * Login with email and password
 */
router.post('/login', async (req: Request, res: Response) => {
  const startTime = Date.now();
  
  try {
    const { email, password, remember } = req.body;

    // Validate input
    if (!email || !password) {
      return res.status(400).json({
        success: false,
        message: 'Email and password are required'
      });
    }

    // Find user
    const user = users.get(email.toLowerCase());
    
    if (!user) {
      // Prevent timing attacks by still hashing
      hashPassword(password);
      return res.status(401).json({
        success: false,
        message: 'Invalid email or password'
      });
    }

    // Verify password
    const [hash, salt] = user.passwordHash.split(':');
    const isValid = verifyPassword(password, hash, salt);

    if (!isValid) {
      return res.status(401).json({
        success: false,
        message: 'Invalid email or password'
      });
    }

    // Generate session token
    const token = generateAuthToken();
    const expiresAt = new Date();
    expiresAt.setHours(expiresAt.getHours() + (remember ? 168 : 24)); // 7 days if remember, else 24 hours

    sessions.set(token, {
      userId: user.id,
      createdAt: new Date(),
      expiresAt
    });

    const loginTime = Date.now() - startTime;

    res.json({
      success: true,
      token,
      user: {
        id: user.id,
        email: user.email,
        name: user.name
      },
      loginTime: loginTime / 1000,
      redirect: '/dashboard'
    });
  } catch (error) {
    console.error('Login error:', error);
    res.status(500).json({
      success: false,
      message: 'Internal server error'
    });
  }
});

/**
 * POST /api/auth/logout
 * Logout and invalidate token
 */
router.post('/logout', (req: Request, res: Response) => {
  try {
    const token = req.headers.authorization?.replace('Bearer ', '');
    
    if (token) {
      sessions.delete(token);
    }

    res.json({
      success: true,
      message: 'Logged out successfully'
    });
  } catch (error) {
    console.error('Logout error:', error);
    res.status(500).json({
      success: false,
      message: 'Internal server error'
    });
  }
});

/**
 * POST /api/auth/verify
 * Verify authentication token
 */
router.post('/verify', (req: Request, res: Response) => {
  try {
    const token = req.headers.authorization?.replace('Bearer ', '');
    
    if (!token) {
      return res.status(401).json({
        success: false,
        message: 'No token provided'
      });
    }

    const session = sessions.get(token);
    
    if (!session) {
      return res.status(401).json({
        success: false,
        message: 'Invalid token'
      });
    }

    // Check if session expired
    if (new Date() > session.expiresAt) {
      sessions.delete(token);
      return res.status(401).json({
        success: false,
        message: 'Token expired'
      });
    }

    // Find user
    const user = Array.from(users.values()).find(u => u.id === session.userId);
    
    if (!user) {
      return res.status(401).json({
        success: false,
        message: 'User not found'
      });
    }

    res.json({
      success: true,
      user: {
        id: user.id,
        email: user.email,
        name: user.name
      }
    });
  } catch (error) {
    console.error('Verify error:', error);
    res.status(500).json({
      success: false,
      message: 'Internal server error'
    });
  }
});

/**
 * POST /api/auth/webauthn/challenge
 * Get WebAuthn authentication challenge
 */
router.post('/webauthn/challenge', (req: Request, res: Response) => {
  try {
    // Generate a random challenge
    const challenge = crypto.randomBytes(32).toString('base64');
    
    // Store challenge temporarily (in production, use Redis with expiration)
    // For now, we'll just return it
    
    res.json({
      success: true,
      publicKey: {
        challenge: challenge,
        timeout: 60000,
        rpId: req.hostname,
        allowCredentials: [], // In production, retrieve user's registered credentials
        userVerification: 'preferred'
      }
    });
  } catch (error) {
    console.error('WebAuthn challenge error:', error);
    res.status(500).json({
      success: false,
      message: 'Failed to generate challenge'
    });
  }
});

/**
 * POST /api/auth/webauthn/verify
 * Verify WebAuthn authentication
 */
router.post('/webauthn/verify', (req: Request, res: Response) => {
  try {
    const { id, rawId, response, type } = req.body;

    // In production, verify the signature using the stored public key
    // For demo purposes, we'll simulate success
    
    // Generate session token
    const token = generateAuthToken();
    const expiresAt = new Date();
    expiresAt.setHours(expiresAt.getHours() + 24);

    // Use demo user for WebAuthn demo
    const demoUser = users.get('demo@example.com');
    
    if (demoUser) {
      sessions.set(token, {
        userId: demoUser.id,
        createdAt: new Date(),
        expiresAt
      });

      res.json({
        success: true,
        token,
        user: {
          id: demoUser.id,
          email: demoUser.email,
          name: demoUser.name
        },
        redirect: '/dashboard'
      });
    } else {
      res.status(401).json({
        success: false,
        message: 'WebAuthn verification failed'
      });
    }
  } catch (error) {
    console.error('WebAuthn verify error:', error);
    res.status(500).json({
      success: false,
      message: 'Failed to verify WebAuthn'
    });
  }
});

/**
 * GET /api/auth/me
 * Get current user info
 */
router.get('/me', (req: Request, res: Response) => {
  try {
    const token = req.headers.authorization?.replace('Bearer ', '');
    
    if (!token) {
      return res.status(401).json({
        success: false,
        message: 'No token provided'
      });
    }

    const session = sessions.get(token);
    
    if (!session || new Date() > session.expiresAt) {
      return res.status(401).json({
        success: false,
        message: 'Invalid or expired token'
      });
    }

    const user = Array.from(users.values()).find(u => u.id === session.userId);
    
    if (!user) {
      return res.status(404).json({
        success: false,
        message: 'User not found'
      });
    }

    res.json({
      success: true,
      user: {
        id: user.id,
        email: user.email,
        name: user.name
      }
    });
  } catch (error) {
    console.error('Get user error:', error);
    res.status(500).json({
      success: false,
      message: 'Internal server error'
    });
  }
});

export const authRoutes = router;
