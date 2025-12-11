# User Settings Page

The User Settings page provides a web interface for Discord users to configure their preferences for the Sovereignty Architecture Control Plane.

## Features

- **User Profile Management**: Configure Discord user ID and username
- **Notification Preferences**: Toggle notifications for:
  - Pull Requests
  - Deployments
  - Alerts
- **Theme Selection**: Choose between Light and Dark themes
- **Persistent Storage**: Settings are saved to `user-settings.json`

## Endpoints

### Web Interface

- **GET `/settings`**: Display the settings page
  - Query params: `?userId=<discord_user_id>` to load existing settings
  - Example: `http://localhost:3001/settings?userId=123456789`

### API Endpoints

- **POST `/settings`**: Save user settings
  - Content-Type: `application/json`
  - Body:
    ```json
    {
      "userId": "123456789",
      "username": "example_user",
      "preferences": {
        "notifications": {
          "prs": true,
          "deployments": true,
          "alerts": false
        },
        "channels": {
          "preferred": []
        },
        "theme": "dark"
      }
    }
    ```

- **GET `/settings/api/:userId`**: Retrieve settings for a specific user
  - Example: `http://localhost:3001/settings/api/123456789`
  - Returns: User settings JSON

- **GET `/settings/all`**: Retrieve all user settings (admin only)
  - Returns: All user settings as JSON object

## Usage

### Start the Event Gateway

```bash
# Development mode
npm run dev

# Production mode
npm run build
npm start
```

The settings page will be available at: `http://localhost:3001/settings`

### Configure User Settings

1. Navigate to `http://localhost:3001/settings`
2. Enter your Discord User ID
3. Enter your Discord Username
4. Configure notification preferences
5. Select your preferred theme
6. Click "Save Settings"

Your settings will be persisted to the `user-settings.json` file and automatically loaded on subsequent visits.

## Data Storage

User settings are stored in `user-settings.json` in the project root directory. This file is excluded from version control via `.gitignore`.

### Example Storage Format

```json
{
  "123456789": {
    "userId": "123456789",
    "username": "example_user",
    "preferences": {
      "notifications": {
        "prs": true,
        "deployments": true,
        "alerts": true
      },
      "channels": {
        "preferred": []
      },
      "theme": "light"
    },
    "updatedAt": "2025-12-11T00:52:00.000Z"
  }
}
```

## Integration with Discord Bot

The settings can be queried by the Discord bot to customize notifications per user. For example:

```typescript
import { getSettingsAPI } from "./routes/settings.js";

// In your Discord bot code
const userId = interaction.user.id;
const response = await fetch(`http://localhost:3001/settings/api/${userId}`);
const settings = await response.json();

// Check if user wants PR notifications
if (settings.preferences.notifications.prs) {
  // Send PR notification
}
```

## Security Considerations

- In production, implement authentication and authorization
- Consider rate limiting for API endpoints
- Use HTTPS for secure data transmission
- Validate and sanitize all user inputs
- Implement CSRF protection for form submissions

## Future Enhancements

- Add user authentication via Discord OAuth2
- Implement channel preference management
- Add email notification options
- Create admin dashboard for user management
- Add export/import settings functionality
- Implement settings versioning
