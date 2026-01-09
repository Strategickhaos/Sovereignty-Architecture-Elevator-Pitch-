import type { Request, Response, Router } from "express";
import { readFileSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

interface SignupData {
  username: string;
  email: string;
  password: string;
  plan: string;
}

// Email validation regex - basic validation
// Note: This is a simplified regex and may not catch all edge cases.
// In production, consider using a more robust validation library.
const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

// Username validation: 3-30 characters, alphanumeric with underscores and hyphens
// Note: This pattern is duplicated in signup.html for client-side validation
const USERNAME_REGEX = /^[a-zA-Z0-9_-]{3,30}$/;

// Valid plans
const VALID_PLANS = ['free', 'sync', 'speed', 'power'];

function validateSignupData(data: SignupData): { valid: boolean; error?: string } {
  if (!data.username?.trim() || !data.email?.trim() || !data.password || !data.plan) {
    return { valid: false, error: 'All fields are required' };
  }

  if (!USERNAME_REGEX.test(data.username.trim())) {
    return { valid: false, error: 'Invalid username format' };
  }

  if (!EMAIL_REGEX.test(data.email.trim())) {
    return { valid: false, error: 'Invalid email address' };
  }

  if (data.password.length < 8) {
    return { valid: false, error: 'Password must be at least 8 characters long' };
  }

  if (!VALID_PLANS.includes(data.plan)) {
    return { valid: false, error: 'Invalid plan selected' };
  }

  return { valid: true };
}

export function setupSignupRoutes(router: Router) {
  // GET /signup - Serve the signup form
  router.get('/signup', (req: Request, res: Response) => {
    try {
      const htmlPath = join(__dirname, '..', 'views', 'signup.html');
      const html = readFileSync(htmlPath, 'utf-8');
      res.setHeader('Content-Type', 'text/html');
      res.send(html);
    } catch (error) {
      console.error('Error serving signup form:', error);
      res.status(500).send('Internal server error');
    }
  });

  // POST /signup - Handle registration
  router.post('/signup', async (req: Request, res: Response) => {
    try {
      const signupData: SignupData = req.body;

      // Validate input
      const validation = validateSignupData(signupData);
      if (!validation.valid) {
        return res.status(400).json({ error: validation.error });
      }

      // In a real application, you would:
      // 1. Check if username/email already exists
      // 2. Hash the password
      // 3. Save to database
      // 4. Send confirmation email
      // 5. Create session/JWT token

      // For now, we'll just log and return success
      // Note: In production, log only non-PII data
      console.log('New user registration:', {
        plan: signupData.plan,
        timestamp: new Date().toISOString()
      });

      // Simulate checking for duplicate users (in real app, check database)
      // For demo purposes, we'll accept all registrations

      // Trim whitespace from username and email
      const cleanUsername = signupData.username.trim();
      const cleanEmail = signupData.email.trim();

      res.status(201).json({
        success: true,
        message: 'Account created successfully!',
        redirect: '/dashboard',
        user: {
          username: cleanUsername,
          email: cleanEmail,
          plan: signupData.plan
        }
      });
    } catch (error) {
      console.error('Error processing signup:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  });
}
