# User Registration Form

This document describes the user registration feature added to the Sovereignty Architecture.

## Overview

A complete user registration system has been added to the Express-based event gateway application. The feature includes:
- A responsive HTML registration form
- Backend validation and processing
- Integration with the existing Express application

## Files Added

### Frontend
- **`src/views/signup.html`** - Standalone HTML page with embedded CSS and JavaScript
  - Responsive design with gradient background
  - Form validation (client-side)
  - Plan selection with dynamic descriptions
  - Success/error message display
  - Pre-selects plan from URL parameter (e.g., `/signup?plan=sync`)

### Backend
- **`src/routes/signup.ts`** - TypeScript route handlers
  - `GET /signup` - Serves the HTML registration form
  - `POST /signup` - Processes registration data with validation
  - Validates username (3-30 chars, alphanumeric with `-` and `_`)
  - Validates email format
  - Validates password (minimum 8 characters)
  - Validates plan selection (free, sync, speed, power)

### Integration
- **`src/event-gateway.ts`** - Updated to include signup routes
  - Added import for `setupSignupRoutes`
  - Called `setupSignupRoutes(app)` to register routes

## Usage

### Accessing the Form
Navigate to: `http://localhost:3001/signup`

Or with a pre-selected plan: `http://localhost:3001/signup?plan=sync`

### Form Fields
- **Username**: 3-30 characters, letters, numbers, underscores, and hyphens
- **Email**: Valid email address format
- **Password**: Minimum 8 characters
- **Confirm Password**: Must match password
- **Plan**: Select from free, sync ($9/mo), speed ($19/mo), or power ($29/mo)

### API Endpoint

**POST /signup**

Request body:
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepass123",
  "plan": "sync"
}
```

Success response (201):
```json
{
  "success": true,
  "message": "Account created successfully!",
  "redirect": "/dashboard",
  "user": {
    "username": "johndoe",
    "email": "john@example.com",
    "plan": "sync"
  }
}
```

Error response (400):
```json
{
  "error": "Invalid email address"
}
```

## Implementation Notes

### Current State
The implementation currently logs registrations to the console and returns a success response. It does NOT:
- Store data in a database
- Hash passwords
- Check for duplicate users
- Send confirmation emails
- Create sessions or tokens

### Future Enhancements
To make this production-ready, you would need to:
1. Add database integration to store user data
2. Hash passwords using bcrypt or similar
3. Check for duplicate usernames/emails
4. Implement email verification
5. Create authentication sessions (JWT or session cookies)
6. **Add rate limiting to prevent abuse (both GET and POST endpoints)**
7. Add CAPTCHA for bot prevention
8. Implement proper error handling and logging
9. Cache the HTML form in memory instead of reading from disk on every request

## Security Considerations

The current implementation includes:
- Server-side validation of all inputs
- Client-side validation for better UX
- Password minimum length requirement
- Pattern validation for username
- PII data excluded from logs

**Security Concerns Identified:**
- **Rate Limiting**: The signup endpoints (both GET and POST) are not rate-limited, which could allow abuse. In production, implement rate limiting using a middleware like `express-rate-limit`.
- **File System Access**: The HTML form is read from disk on every request, which could be a performance concern. Consider caching the HTML in memory.
- **Password Storage**: Passwords are not currently hashed (as this is a demo implementation).
- **Email Validation**: Basic regex validation may not catch all edge cases.
- **No CAPTCHA**: Vulnerable to automated bot registrations.

## Design Choices

1. **Standalone HTML**: The form is a complete standalone HTML file with embedded CSS and JavaScript for easy deployment and minimal dependencies.

2. **Plan Selection**: Integrated with the existing landing page which references plans like "sync" and "speed".

3. **TypeScript**: Maintained consistency with the existing codebase by using TypeScript for the backend.

4. **Minimal Changes**: Only added necessary files and made minimal modifications to existing code (3 lines added to event-gateway.ts).

## Testing

Since there is no existing test infrastructure in the repository, manual testing is recommended:

1. Start the server: `npm run dev`
2. Navigate to `http://localhost:3001/signup`
3. Test form validation by:
   - Leaving fields empty
   - Entering mismatched passwords
   - Using invalid email formats
   - Using short passwords
4. Test successful registration with valid data
5. Check console output for logged registration data

## Integration with Landing Page

The landing page (`contradictions/landing_sections.html`) already has links to `/signup?plan=sync` and `/signup?plan=speed`. The new form automatically pre-selects the plan from the URL parameter, creating a seamless user experience.
