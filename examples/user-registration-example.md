# User Registration Feature - Usage Examples

## Discord Bot Command

### Register a new user with email
```
/register username:john_doe email:john@example.com
```

Response (ephemeral):
```
✅ Registration Successful
Welcome, john_doe!
User ID: 550e8400-e29b-41d4-a716-446655440000
Discord ID: 123456789012345678
Email: john@example.com
Registered: 2025-12-13T04:20:00.000Z
```

### Register without email
```
/register username:jane_smith
```

Response (ephemeral):
```
✅ Registration Successful
Welcome, jane_smith!
User ID: 660e9511-f30c-52e5-b827-557766551111
Discord ID: 987654321098765432
Registered: 2025-12-13T04:21:00.000Z
```

### Duplicate registration attempt
```
/register username:john_doe
```

Response (ephemeral):
```
❌ You are already registered!
```

## REST API Examples

### Register a user via API

```bash
curl -X POST http://localhost:3001/api/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "api_user",
    "discordId": "111222333444555666",
    "email": "api@example.com"
  }'
```

Response (201 Created):
```json
{
  "success": true,
  "user": {
    "id": "770fa622-g41d-63f6-c938-668877662222",
    "username": "api_user",
    "discordId": "111222333444555666",
    "email": "api@example.com",
    "roles": [],
    "createdAt": "2025-12-13T04:22:00.000Z",
    "updatedAt": "2025-12-13T04:22:00.000Z"
  }
}
```

### Get user by Discord ID

```bash
curl http://localhost:3001/api/users/111222333444555666
```

Response (200 OK):
```json
{
  "success": true,
  "user": {
    "id": "770fa622-g41d-63f6-c938-668877662222",
    "username": "api_user",
    "discordId": "111222333444555666",
    "email": "api@example.com",
    "roles": [],
    "createdAt": "2025-12-13T04:22:00.000Z",
    "updatedAt": "2025-12-13T04:22:00.000Z"
  }
}
```

### List all users

```bash
curl http://localhost:3001/api/users
```

Response (200 OK):
```json
{
  "success": true,
  "users": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "username": "john_doe",
      "discordId": "123456789012345678",
      "email": "john@example.com",
      "roles": [],
      "createdAt": "2025-12-13T04:20:00.000Z",
      "updatedAt": "2025-12-13T04:20:00.000Z"
    },
    {
      "id": "660e9511-f30c-52e5-b827-557766551111",
      "username": "jane_smith",
      "discordId": "987654321098765432",
      "roles": [],
      "createdAt": "2025-12-13T04:21:00.000Z",
      "updatedAt": "2025-12-13T04:21:00.000Z"
    },
    {
      "id": "770fa622-g41d-63f6-c938-668877662222",
      "username": "api_user",
      "discordId": "111222333444555666",
      "email": "api@example.com",
      "roles": [],
      "createdAt": "2025-12-13T04:22:00.000Z",
      "updatedAt": "2025-12-13T04:22:00.000Z"
    }
  ],
  "count": 3
}
```

## Error Responses

### Invalid username (too short)
```bash
curl -X POST http://localhost:3001/api/users/register \
  -H "Content-Type: application/json" \
  -d '{"username": "ab", "discordId": "123"}'
```

Response (400 Bad Request):
```json
{
  "success": false,
  "error": "Invalid input",
  "details": [
    {
      "code": "too_small",
      "minimum": 3,
      "type": "string",
      "path": ["username"],
      "message": "String must contain at least 3 character(s)"
    }
  ]
}
```

### Duplicate Discord ID
```bash
curl -X POST http://localhost:3001/api/users/register \
  -H "Content-Type: application/json" \
  -d '{"username": "duplicate", "discordId": "123456789012345678"}'
```

Response (409 Conflict):
```json
{
  "success": false,
  "error": "User already registered"
}
```

### User not found
```bash
curl http://localhost:3001/api/users/999999999999999999
```

Response (404 Not Found):
```json
{
  "success": false,
  "error": "User not found"
}
```

## Integration with Existing Commands

Once registered, users can be tracked across all Discord bot interactions:

```
/status service:quantum-emulator
/deploy env:dev tag:v1.2.3
/scale service:api replicas:5
```

All commands now associate with the registered user's Discord ID for audit logging and access control.
