# Login Functionality Documentation

## Overview

This implementation adds a complete login and authentication system to the Sovereignty Architecture platform, featuring:

- Modern, responsive login page with password visibility toggle
- WebAuthn support for passwordless authentication
- Session-based authentication with token management
- Login time tracking (targeting < 1.2s as per design specifications)
- Secure password hashing using PBKDF2
- Protected dashboard area
- RESTful authentication API

## Features

### 1. Login Page (`/login`)

A beautiful, modern login interface with:
- Email/username and password fields
- "Remember me" checkbox for extended sessions
- Password visibility toggle
- Forgot password link (placeholder)
- WebAuthn one-click login
- Real-time login time metrics
- Smooth animations and transitions
- Mobile-responsive design

**Demo Credentials:**
- Email: `demo@example.com`
- Password: `demo123`

### 2. Authentication API

#### POST `/api/auth/login`
Login with email and password.

**Request:**
```json
{
  "email": "demo@example.com",
  "password": "demo123",
  "remember": false
}
```

**Response (Success):**
```json
{
  "success": true,
  "token": "auth_token_here",
  "user": {
    "id": "user-id",
    "email": "demo@example.com",
    "name": "Demo User"
  },
  "loginTime": 0.05,
  "redirect": "/dashboard"
}
```

#### POST `/api/auth/logout`
Logout and invalidate token.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

#### POST `/api/auth/verify`
Verify authentication token.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true,
  "user": {
    "id": "user-id",
    "email": "demo@example.com",
    "name": "Demo User"
  }
}
```

#### GET `/api/auth/me`
Get current user information.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true,
  "user": {
    "id": "user-id",
    "email": "demo@example.com",
    "name": "Demo User"
  }
}
```

### 3. WebAuthn Support

#### POST `/api/auth/webauthn/challenge`
Request authentication challenge for WebAuthn.

**Response:**
```json
{
  "success": true,
  "publicKey": {
    "challenge": "base64_encoded_challenge",
    "timeout": 60000,
    "rpId": "yourdomain.com",
    "allowCredentials": [],
    "userVerification": "preferred"
  }
}
```

#### POST `/api/auth/webauthn/verify`
Verify WebAuthn authentication response.

**Request:**
```json
{
  "id": "credential_id",
  "rawId": "base64_raw_id",
  "response": {
    "authenticatorData": "base64_data",
    "clientDataJSON": "base64_json",
    "signature": "base64_signature",
    "userHandle": "base64_handle"
  },
  "type": "public-key"
}
```

### 4. Dashboard (`/dashboard`)

Protected dashboard page that:
- Verifies authentication on load
- Displays user information
- Shows available platform features
- Provides logout functionality
- Auto-redirects to login if not authenticated

### 5. Authentication Middleware

Two middleware functions for protecting routes:

```typescript
import { requireAuth, optionalAuth } from './middleware/auth.js';

// Require authentication
app.get('/protected', requireAuth, (req, res) => {
  // req.user is available here
  res.json({ user: req.user });
});

// Optional authentication
app.get('/public', optionalAuth, (req, res) => {
  // req.user is available if authenticated, undefined otherwise
  res.json({ user: req.user || null });
});
```

## Security Features

1. **Password Hashing**: Uses PBKDF2 with 10,000 iterations and SHA-512
2. **Session Management**: Time-limited sessions (24h default, 7 days with "remember me")
3. **Token-Based Auth**: Cryptographically secure random tokens (32 bytes)
4. **Timing Attack Prevention**: Consistent response times for invalid logins
5. **HTTPS Ready**: All authentication should be done over HTTPS in production
6. **WebAuthn**: Passwordless authentication with biometric/hardware keys

## Running the Application

1. **Install dependencies:**
```bash
npm install
```

2. **Start the development server:**
```bash
npm run dev
```

3. **Access the login page:**
```
http://localhost:3001/
http://localhost:3001/login
```

4. **Login with demo credentials:**
- Email: `demo@example.com`
- Password: `demo123`

5. **View the dashboard:**
```
http://localhost:3001/dashboard
```

## File Structure

```
public/
├── login.html          # Login page with WebAuthn support
└── dashboard.html      # Protected dashboard page

src/
├── event-gateway.ts    # Main application with auth routes
├── routes/
│   ├── auth.ts         # Authentication API routes
│   └── github.ts       # Existing GitHub webhook routes
└── middleware/
    └── auth.ts         # Authentication middleware
```

## Production Considerations

⚠️ **This is a demonstration implementation**. For production use, consider:

1. **Database Integration**: Replace in-memory stores with PostgreSQL/MongoDB
2. **Redis Sessions**: Use Redis for distributed session management
3. **JWT Tokens**: Consider JWT for stateless authentication
4. **Rate Limiting**: Add rate limiting to prevent brute force attacks
5. **2FA**: Implement two-factor authentication
6. **Email Verification**: Add email verification for new accounts
7. **Password Reset**: Implement secure password reset flow
8. **Audit Logging**: Log all authentication events
9. **HTTPS**: Always use HTTPS in production
10. **WebAuthn Implementation**: Complete WebAuthn server-side verification
11. **CORS Configuration**: Properly configure CORS for API access
12. **Environment Variables**: Store secrets securely (not in code)

## Performance

The implementation is designed to meet the "Login in 1.2s" requirement:

- Minimal dependencies and lightweight code
- Efficient password hashing (configurable iterations)
- In-memory session storage (very fast)
- Client-side time tracking and display
- WebAuthn for even faster biometric login

## Testing

To test the login functionality:

1. **Standard Login:**
   - Navigate to `/login`
   - Enter email: `demo@example.com`
   - Enter password: `demo123`
   - Click "Sign In"
   - Observe login time displayed
   - Verify redirect to dashboard

2. **WebAuthn Login:**
   - Click "Sign in with WebAuthn"
   - Follow browser prompts (if WebAuthn is configured)
   - Verify redirect to dashboard

3. **Protected Routes:**
   - Try accessing `/dashboard` without logging in
   - Should redirect to login page
   - Login and verify dashboard access

4. **Logout:**
   - Click "Logout" button in dashboard
   - Verify redirect to login page
   - Verify cannot access dashboard without re-login

## API Testing with curl

```bash
# Login
curl -X POST http://localhost:3001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@example.com","password":"demo123","remember":false}'

# Verify token (replace TOKEN with actual token from login)
curl -X POST http://localhost:3001/api/auth/verify \
  -H "Authorization: Bearer TOKEN"

# Get current user
curl -X GET http://localhost:3001/api/auth/me \
  -H "Authorization: Bearer TOKEN"

# Logout
curl -X POST http://localhost:3001/api/auth/logout \
  -H "Authorization: Bearer TOKEN"
```

## Future Enhancements

- [ ] User registration endpoint
- [ ] Complete password reset flow
- [ ] Social login (OAuth) integration
- [ ] Two-factor authentication (TOTP)
- [ ] Full WebAuthn implementation with credential storage
- [ ] Account management page
- [ ] Login history and security logs
- [ ] Device management
- [ ] API key generation for programmatic access
- [ ] Role-based access control (RBAC) integration
