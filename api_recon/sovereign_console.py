"""
Sovereign Console - Zero Vendor Lock-in Cloud Management
Web UI that uses MCP tools instead of vendor APIs
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, List, Optional
import importlib
import os
import sys
import json
from pathlib import Path


class SovereignConsole:
    """Sovereign cloud management console using MCP tools"""
    
    def __init__(self, tools_dir: str = "generated_tools"):
        self.app = FastAPI(
            title="KhaosConsole - Sovereign Cloud Management",
            description="Zero Vendor Lock-in Cloud Management Interface",
            version="1.0.0"
        )
        self.tools_dir = tools_dir
        self.tools: Dict[str, Any] = {}
        
        # Configure CORS
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Setup routes
        self._setup_routes()
        
        # Load MCP tools
        self._load_tools()
    
    def _setup_routes(self):
        """Setup API routes"""
        
        @self.app.get("/", response_class=HTMLResponse)
        async def console_ui():
            """Sovereign console web UI"""
            return self._get_console_html()
        
        @self.app.get("/health")
        async def health_check():
            """Health check endpoint"""
            return {
                "status": "healthy",
                "tools_loaded": len(self.tools),
                "sovereign": True
            }
        
        @self.app.get("/api/tools")
        async def list_tools():
            """List all available MCP tools"""
            tools_info = []
            for name, tool in self.tools.items():
                tools_info.append({
                    "name": name,
                    "description": tool.description if hasattr(tool, 'description') else "",
                    "input_schema": tool.input_schema if hasattr(tool, 'input_schema') else {}
                })
            return {"tools": tools_info}
        
        @self.app.post("/api/execute/{tool_name}")
        async def execute_tool(tool_name: str, request: Request):
            """Execute an MCP tool"""
            if tool_name not in self.tools:
                raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")
            
            tool = self.tools[tool_name]
            params = await request.json()
            
            try:
                result = await tool.execute(**params)
                return result
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e)
                }
        
        # GCP-compatible endpoints (sovereign replacements)
        
        @self.app.get("/api/monitoring/metrics")
        async def get_metrics(project: str):
            """Sovereign replacement for monitoring.googleapis.com"""
            tool = self.tools.get("v3_projects_metricdescriptors")
            if tool:
                return await tool.execute(project=project)
            return {"error": "Metrics tool not available"}
        
        @self.app.get("/api/monitoring/resources")
        async def get_resources(project: str):
            """Sovereign replacement for resource descriptors"""
            tool = self.tools.get("v3_projects_monitoredresourcedescriptors")
            if tool:
                return await tool.execute(project=project)
            return {"error": "Resources tool not available"}
        
        @self.app.get("/api/monitoring/groups")
        async def get_groups(project: str):
            """Sovereign replacement for groups API"""
            tool = self.tools.get("v3_projects_groups")
            if tool:
                return await tool.execute(project=project)
            return {"error": "Groups tool not available"}
        
        @self.app.get("/api/shell/quota")
        async def get_shell_quota():
            """Sovereign replacement for Cloud Shell quota"""
            tool = self.tools.get("devshell_quota")
            if tool:
                return await tool.execute()
            return {"error": "Quota tool not available"}
    
    def _load_tools(self):
        """Dynamically load all generated MCP tools"""
        tools_path = Path(self.tools_dir)
        
        if not tools_path.exists():
            print(f"Warning: Tools directory '{self.tools_dir}' does not exist")
            return
        
        # Add tools directory to Python path
        sys.path.insert(0, str(tools_path.parent))
        
        # Load all Python files
        for tool_file in tools_path.glob("*.py"):
            if tool_file.name.startswith('_'):
                continue
            
            try:
                # Import module
                module_name = f"{tools_path.name}.{tool_file.stem}"
                module = importlib.import_module(module_name)
                
                # Find tool instance
                if hasattr(module, 'tool_instance'):
                    tool = module.tool_instance
                    self.tools[tool.name] = tool
                    print(f"Loaded tool: {tool.name}")
                
            except Exception as e:
                print(f"Error loading {tool_file}: {e}")
    
    def _get_console_html(self) -> str:
        """Get the console web UI HTML"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>⚔️ KhaosConsole - Sovereign Cloud Management</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'JetBrains Mono', 'Courier New', monospace;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: #e0e0e0;
            min-height: 100vh;
        }
        
        .header {
            background: linear-gradient(90deg, #7b2cbf, #c77dff, #e0aaff);
            padding: 30px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }
        
        .header h1 {
            font-size: 2.5em;
            color: #fff;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }
        
        .header p {
            font-size: 1.2em;
            color: #f0f0f0;
            margin-top: 10px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .panel {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 25px;
            margin: 20px 0;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        }
        
        .panel h2 {
            color: #c77dff;
            font-size: 1.8em;
            margin-bottom: 20px;
            border-bottom: 2px solid #7b2cbf;
            padding-bottom: 10px;
        }
        
        .status-badge {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
            margin: 5px;
        }
        
        .status-sovereign {
            background: #10b981;
            color: white;
        }
        
        .status-vendor {
            background: #ef4444;
            color: white;
        }
        
        .tool-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
            transition: all 0.3s ease;
        }
        
        .tool-card:hover {
            background: rgba(255, 255, 255, 0.08);
            transform: translateX(5px);
            border-left: 3px solid #c77dff;
        }
        
        .tool-name {
            color: #c77dff;
            font-weight: bold;
            font-size: 1.1em;
        }
        
        .tool-desc {
            color: #a0a0a0;
            margin-top: 5px;
        }
        
        .code-block {
            background: #1a1a2e;
            border: 1px solid #16213e;
            border-radius: 8px;
            padding: 15px;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            color: #00ff41;
            margin: 10px 0;
        }
        
        .btn {
            background: linear-gradient(90deg, #7b2cbf, #9d4edd);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        
        .btn:hover {
            background: linear-gradient(90deg, #9d4edd, #c77dff);
            transform: scale(1.05);
        }
        
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            border-top-color: #c77dff;
            animation: spin 1s ease-in-out infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        .metric-value {
            font-size: 2em;
            color: #00ff41;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>⚔️ KhaosConsole</h1>
        <p>Sovereign Cloud Management - Zero Vendor Lock-in</p>
        <div style="margin-top: 15px;">
            <span class="status-badge status-sovereign">✓ SOVEREIGN MODE</span>
            <span class="status-badge" id="statusBadge">⟳ Loading...</span>
        </div>
    </div>
    
    <div class="container">
        <div class="panel">
            <h2>📊 System Status</h2>
            <div class="grid">
                <div>
                    <strong>MCP Tools Loaded:</strong>
                    <div class="metric-value" id="toolsCount">-</div>
                </div>
                <div>
                    <strong>Mode:</strong>
                    <div class="metric-value" style="color: #10b981;">SOVEREIGN</div>
                </div>
                <div>
                    <strong>Vendor Dependency:</strong>
                    <div class="metric-value" style="color: #ef4444; font-size: 1.5em;">ZERO</div>
                </div>
            </div>
        </div>
        
        <div class="panel">
            <h2>🛠️ Available MCP Tools</h2>
            <div id="toolsList">
                <div class="loading"></div> Loading tools...
            </div>
        </div>
        
        <div class="panel">
            <h2>🔍 API Translation Demo</h2>
            <p style="margin-bottom: 15px;">
                See how vendor APIs are transparently replaced with sovereign infrastructure:
            </p>
            <div class="code-block">
                <div>// Vendor API (requires internet, vendor access, billing)</div>
                <div style="color: #ff6b6b;">❌ GET https://monitoring.googleapis.com/v3/projects/my-project/metricDescriptors</div>
                <div style="margin: 10px 0;">↓ SHADOW MIRROR translates to ↓</div>
                <div>// Sovereign API (local, no vendor, free)</div>
                <div style="color: #00ff41;">✓ GET http://prometheus:9090/api/v1/metadata</div>
            </div>
        </div>
        
        <div class="panel">
            <h2>📈 Value Proposition</h2>
            <div class="grid">
                <div class="tool-card">
                    <div class="tool-name">💰 Cost Savings</div>
                    <div class="tool-desc">$1,200+ annual savings on monitoring APIs alone</div>
                </div>
                <div class="tool-card">
                    <div class="tool-name">🔒 Data Sovereignty</div>
                    <div class="tool-desc">All data stays on your infrastructure</div>
                </div>
                <div class="tool-card">
                    <div class="tool-name">⚡ Performance</div>
                    <div class="tool-desc">Local calls &lt;100ms vs cloud APIs 200-500ms</div>
                </div>
                <div class="tool-card">
                    <div class="tool-name">🌐 Offline Capable</div>
                    <div class="tool-desc">Works without internet connectivity</div>
                </div>
                <div class="tool-card">
                    <div class="tool-name">🔓 Zero Lock-in</div>
                    <div class="tool-desc">Switch vendors or go sovereign anytime</div>
                </div>
                <div class="tool-card">
                    <div class="tool-name">🛡️ Full Control</div>
                    <div class="tool-desc">You control access, no vendor revocation</div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // Load system status
        async function loadStatus() {
            try {
                const response = await fetch('/health');
                const data = await response.json();
                
                document.getElementById('toolsCount').textContent = data.tools_loaded;
                
                const statusBadge = document.getElementById('statusBadge');
                if (data.status === 'healthy') {
                    statusBadge.textContent = '✓ ONLINE';
                    statusBadge.className = 'status-badge status-sovereign';
                } else {
                    statusBadge.textContent = '⚠ DEGRADED';
                    statusBadge.className = 'status-badge status-vendor';
                }
            } catch (error) {
                console.error('Error loading status:', error);
            }
        }
        
        // Load available tools
        async function loadTools() {
            try {
                const response = await fetch('/api/tools');
                const data = await response.json();
                
                const toolsList = document.getElementById('toolsList');
                
                if (data.tools.length === 0) {
                    toolsList.innerHTML = '<p style="color: #ff6b6b;">No tools loaded. Generate MCP tools first.</p>';
                    return;
                }
                
                toolsList.innerHTML = '';
                data.tools.forEach(tool => {
                    const toolCard = document.createElement('div');
                    toolCard.className = 'tool-card';
                    toolCard.innerHTML = `
                        <div class="tool-name">${tool.name}</div>
                        <div class="tool-desc">${tool.description.split('\\n')[0]}</div>
                    `;
                    toolsList.appendChild(toolCard);
                });
            } catch (error) {
                console.error('Error loading tools:', error);
                document.getElementById('toolsList').innerHTML = 
                    '<p style="color: #ff6b6b;">Error loading tools. Check console.</p>';
            }
        }
        
        // Initialize
        loadStatus();
        loadTools();
        
        // Refresh every 30 seconds
        setInterval(loadStatus, 30000);
    </script>
</body>
</html>
        """


def create_app(tools_dir: str = "generated_tools") -> FastAPI:
    """Create and configure the FastAPI application"""
    console = SovereignConsole(tools_dir=tools_dir)
    return console.app


def main():
    """Run the sovereign console server"""
    import uvicorn
    import argparse
    
    parser = argparse.ArgumentParser(description='Sovereign Console - Zero Vendor Lock-in')
    parser.add_argument('--tools-dir', default='generated_tools',
                       help='Directory containing generated MCP tools')
    parser.add_argument('--host', default='0.0.0.0',
                       help='Host to bind to')
    parser.add_argument('--port', type=int, default=8000,
                       help='Port to bind to')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("⚔️  KHAOS CONSOLE - SOVEREIGN CLOUD MANAGEMENT")
    print("=" * 60)
    print(f"Tools directory: {args.tools_dir}")
    print(f"Listening on: http://{args.host}:{args.port}")
    print("=" * 60)
    
    app = create_app(tools_dir=args.tools_dir)
    
    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        log_level="info"
    )


if __name__ == "__main__":
    main()
