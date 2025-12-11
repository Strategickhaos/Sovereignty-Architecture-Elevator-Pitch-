import type { Request, Response } from "express";
import fs from "fs";
import path from "path";

// User settings interface
interface UserSettings {
  userId: string;
  username: string;
  preferences: {
    notifications: {
      prs: boolean;
      deployments: boolean;
      alerts: boolean;
    };
    channels: {
      preferred: string[];
    };
    theme: "light" | "dark";
  };
  updatedAt: string;
}

// Simple in-memory storage (in production, use a database)
const settingsStore = new Map<string, UserSettings>();

// Load settings from file if exists
const SETTINGS_FILE = path.join(process.cwd(), "user-settings.json");
function loadSettings() {
  try {
    if (fs.existsSync(SETTINGS_FILE)) {
      const data = JSON.parse(fs.readFileSync(SETTINGS_FILE, "utf8"));
      Object.entries(data).forEach(([key, value]) => {
        settingsStore.set(key, value as UserSettings);
      });
    }
  } catch (err) {
    console.error("Failed to load settings:", err);
  }
}

// Save settings to file
function saveSettings() {
  try {
    const data = Object.fromEntries(settingsStore);
    fs.writeFileSync(SETTINGS_FILE, JSON.stringify(data, null, 2));
  } catch (err) {
    console.error("Failed to save settings:", err);
  }
}

// Initialize settings
loadSettings();

// HTML template for settings page
function settingsPageHTML(userId?: string, settings?: UserSettings) {
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>User Settings - Sovereignty Architecture</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      min-height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 20px;
    }
    .container {
      background: white;
      border-radius: 12px;
      box-shadow: 0 20px 60px rgba(0,0,0,0.3);
      max-width: 600px;
      width: 100%;
      padding: 40px;
    }
    h1 {
      color: #333;
      margin-bottom: 10px;
      font-size: 28px;
    }
    .subtitle {
      color: #666;
      margin-bottom: 30px;
      font-size: 14px;
    }
    .form-group {
      margin-bottom: 25px;
    }
    label {
      display: block;
      color: #333;
      font-weight: 600;
      margin-bottom: 8px;
      font-size: 14px;
    }
    input[type="text"] {
      width: 100%;
      padding: 12px;
      border: 2px solid #e0e0e0;
      border-radius: 6px;
      font-size: 14px;
      transition: border-color 0.3s;
    }
    input[type="text"]:focus {
      outline: none;
      border-color: #667eea;
    }
    .checkbox-group {
      background: #f8f9fa;
      padding: 15px;
      border-radius: 6px;
      margin-bottom: 15px;
    }
    .checkbox-item {
      display: flex;
      align-items: center;
      margin-bottom: 10px;
    }
    .checkbox-item:last-child {
      margin-bottom: 0;
    }
    input[type="checkbox"] {
      width: 18px;
      height: 18px;
      margin-right: 10px;
      cursor: pointer;
    }
    .checkbox-label {
      color: #555;
      font-weight: normal;
      margin: 0;
      cursor: pointer;
    }
    select {
      width: 100%;
      padding: 12px;
      border: 2px solid #e0e0e0;
      border-radius: 6px;
      font-size: 14px;
      background: white;
      cursor: pointer;
      transition: border-color 0.3s;
    }
    select:focus {
      outline: none;
      border-color: #667eea;
    }
    .button-group {
      display: flex;
      gap: 10px;
      margin-top: 30px;
    }
    button {
      flex: 1;
      padding: 14px;
      border: none;
      border-radius: 6px;
      font-size: 14px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.3s;
    }
    .btn-primary {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
    }
    .btn-primary:hover {
      transform: translateY(-2px);
      box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
    }
    .btn-secondary {
      background: #f0f0f0;
      color: #333;
    }
    .btn-secondary:hover {
      background: #e0e0e0;
    }
    .message {
      padding: 12px;
      border-radius: 6px;
      margin-bottom: 20px;
      font-size: 14px;
    }
    .message.success {
      background: #d4edda;
      color: #155724;
      border: 1px solid #c3e6cb;
    }
    .message.error {
      background: #f8d7da;
      color: #721c24;
      border: 1px solid #f5c6cb;
    }
    .section-title {
      color: #667eea;
      font-size: 16px;
      font-weight: 600;
      margin-bottom: 12px;
      margin-top: 10px;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>🔥 User Settings</h1>
    <p class="subtitle">Sovereignty Architecture Control Plane</p>
    
    ${settings ? `<div class="message success">Settings loaded for user: ${settings.username}</div>` : ''}
    
    <form id="settingsForm" method="POST" action="/settings">
      <div class="form-group">
        <label for="userId">Discord User ID</label>
        <input type="text" id="userId" name="userId" value="${userId || ''}" required 
               placeholder="Enter your Discord user ID">
      </div>
      
      <div class="form-group">
        <label for="username">Username</label>
        <input type="text" id="username" name="username" value="${settings?.username || ''}" required
               placeholder="Your Discord username">
      </div>
      
      <div class="form-group">
        <div class="section-title">Notification Preferences</div>
        <div class="checkbox-group">
          <div class="checkbox-item">
            <input type="checkbox" id="notif-prs" name="notifications.prs" 
                   ${settings?.preferences.notifications.prs !== false ? 'checked' : ''}>
            <label for="notif-prs" class="checkbox-label">Pull Request Notifications</label>
          </div>
          <div class="checkbox-item">
            <input type="checkbox" id="notif-deployments" name="notifications.deployments"
                   ${settings?.preferences.notifications.deployments !== false ? 'checked' : ''}>
            <label for="notif-deployments" class="checkbox-label">Deployment Notifications</label>
          </div>
          <div class="checkbox-item">
            <input type="checkbox" id="notif-alerts" name="notifications.alerts"
                   ${settings?.preferences.notifications.alerts !== false ? 'checked' : ''}>
            <label for="notif-alerts" class="checkbox-label">Alert Notifications</label>
          </div>
        </div>
      </div>
      
      <div class="form-group">
        <label for="theme">Theme</label>
        <select id="theme" name="theme">
          <option value="light" ${settings?.preferences.theme === 'light' ? 'selected' : ''}>Light</option>
          <option value="dark" ${settings?.preferences.theme === 'dark' ? 'selected' : ''}>Dark</option>
        </select>
      </div>
      
      <div class="button-group">
        <button type="submit" class="btn-primary">Save Settings</button>
        <button type="button" class="btn-secondary" onclick="window.location.href='/settings'">Reset</button>
      </div>
    </form>
  </div>
  
  <script>
    // Handle form submission
    document.getElementById('settingsForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      const formData = new FormData(e.target);
      const data = {
        userId: formData.get('userId'),
        username: formData.get('username'),
        preferences: {
          notifications: {
            prs: formData.get('notifications.prs') === 'on',
            deployments: formData.get('notifications.deployments') === 'on',
            alerts: formData.get('notifications.alerts') === 'on'
          },
          channels: {
            preferred: []
          },
          theme: formData.get('theme')
        }
      };
      
      try {
        const response = await fetch('/settings', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data)
        });
        
        if (response.ok) {
          window.location.href = '/settings?userId=' + data.userId + '&saved=true';
        } else {
          alert('Failed to save settings');
        }
      } catch (err) {
        alert('Error: ' + err.message);
      }
    });
  </script>
</body>
</html>`;
}

// GET /settings - Display settings page
export function getSettings(req: Request, res: Response) {
  const userId = req.query.userId as string;
  const saved = req.query.saved as string;
  
  let settings: UserSettings | undefined;
  if (userId) {
    settings = settingsStore.get(userId);
  }
  
  res.setHeader("Content-Type", "text/html");
  res.send(settingsPageHTML(userId, settings));
}

// POST /settings - Save settings
export function postSettings(req: Request, res: Response) {
  try {
    const { userId, username, preferences } = req.body;
    
    if (!userId || !username) {
      return res.status(400).json({ error: "userId and username are required" });
    }
    
    const settings: UserSettings = {
      userId,
      username,
      preferences: {
        notifications: preferences?.notifications || {
          prs: true,
          deployments: true,
          alerts: true
        },
        channels: preferences?.channels || { preferred: [] },
        theme: preferences?.theme || "light"
      },
      updatedAt: new Date().toISOString()
    };
    
    settingsStore.set(userId, settings);
    saveSettings();
    
    res.json({ success: true, settings });
  } catch (err) {
    console.error("Error saving settings:", err);
    res.status(500).json({ error: "Failed to save settings" });
  }
}

// GET /settings/api/:userId - Get settings as JSON
export function getSettingsAPI(req: Request, res: Response) {
  const userId = req.params.userId;
  const settings = settingsStore.get(userId);
  
  if (!settings) {
    return res.status(404).json({ error: "Settings not found" });
  }
  
  res.json(settings);
}

// Export all settings (for admin purposes)
export function getAllSettings(req: Request, res: Response) {
  const allSettings = Object.fromEntries(settingsStore);
  res.json(allSettings);
}
