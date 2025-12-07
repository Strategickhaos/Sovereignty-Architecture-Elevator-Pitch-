"""
MCP Tool Generator
Generates MCP (Model Context Protocol) tools from captured API patterns
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from jinja2 import Template
import json
import re


class MCPGenerator:
    """Generate MCP tools from API patterns"""
    
    # Template for MCP tools
    MCP_TOOL_TEMPLATE = '''"""
Auto-generated MCP Tool from API Recon
Source: {{ source_url }}
Generated: {{ timestamp }}
Classification: SOVEREIGN TOOL
"""

from typing import Any, Dict, Optional
import httpx
import os


class {{ tool_class_name }}:
    """
    MCP Tool: {{ description }}
    
    Original API: {{ original_endpoint }}
    Sovereign Replacement: {{ sovereign_endpoint }}
    """
    
    name = "{{ tool_id }}"
    description = """{{ description }}
    
    This tool replicates the functionality of {{ original_vendor }} APIs
    but routes to sovereign infrastructure with zero vendor lock-in.
    """
    
    input_schema = {
        "type": "object",
        "properties": {
            {% for param in parameters %}
            "{{ param.name }}": {
                "type": "{{ param.type }}",
                "description": "{{ param.description }}"{{ "," if param.required else "" }}
                {% if param.required %}"required": True{% endif %}
            }{{ "," if not loop.last else "" }}
            {% endfor %}
        },
        "required": {{ required_params }}
    }
    
    def __init__(self):
        self.base_url = "{{ sovereign_endpoint }}"
        self.original_url = "{{ original_endpoint }}"
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the sovereign version of this API call"""
        
        # Route to sovereign backend
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.{{ method.lower() }}(
                    self._build_url(**kwargs),
                    headers=self._get_headers(**kwargs),
                    {% if method in ["POST", "PUT", "PATCH"] %}
                    json=self._build_payload(**kwargs)
                    {% else %}
                    params=self._build_params(**kwargs)
                    {% endif %}
                )
                
                response.raise_for_status()
                return {
                    "success": True,
                    "data": response.json() if response.text else {},
                    "status_code": response.status_code,
                    "sovereign": True
                }
                
            except httpx.HTTPStatusError as e:
                return {
                    "success": False,
                    "error": f"HTTP {e.response.status_code}: {e.response.text}",
                    "status_code": e.response.status_code
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e),
                    "status_code": 500
                }
    
    def _build_url(self, **kwargs) -> str:
        """Build the target URL with path parameters"""
        url = self.base_url
        {% for param in path_params %}
        if "{{ param }}" in kwargs:
            url = url.replace("{" + "{{ param }}" + "}", str(kwargs["{{ param }}"]))
        {% endfor %}
        return url
    
    def _get_headers(self, **kwargs) -> Dict[str, str]:
        """Get headers for the request"""
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "KhaosSovereign/1.0"
        }
        
        # Add auth if available
        token = kwargs.get("auth_token") or os.getenv("SOVEREIGN_TOKEN")
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        return headers
    
    def _build_params(self, **kwargs) -> Dict[str, Any]:
        """Build query parameters"""
        params = {}
        {% for param in query_params %}
        if "{{ param }}" in kwargs:
            params["{{ param }}"] = kwargs["{{ param }}"]
        {% endfor %}
        return params
    
    def _build_payload(self, **kwargs) -> Dict[str, Any]:
        """Build request payload for POST/PUT/PATCH"""
        payload = {}
        {% for field in payload_fields %}
        if "{{ field.name }}" in kwargs:
            payload["{{ field.name }}"] = kwargs["{{ field.name }}"]
        {% endfor %}
        return payload


# Register tool for MCP runtime
tool_instance = {{ tool_class_name }}()
'''
    
    # Vendor to sovereign mapping
    SOVEREIGN_MAPPINGS = {
        # GCP Monitoring
        "/v3/projects/{project}/metricDescriptors": {
            "sovereign": "http://prometheus:9090/api/v1/metadata",
            "vendor": "Google Cloud Monitoring"
        },
        "/v3/projects/{project}/groups": {
            "sovereign": "http://khaos-siem:8080/api/groups",
            "vendor": "Google Cloud Monitoring"
        },
        "/v3/projects/{project}/monitoredResourceDescriptors": {
            "sovereign": "http://khaos-siem:8080/api/resources",
            "vendor": "Google Cloud Monitoring"
        },
        
        # GCP Cloud Shell
        "/devshell/quota": {
            "sovereign": "http://queen:8080/api/quota",
            "vendor": "Google Cloud Shell"
        },
        "/cloudshell/environments": {
            "sovereign": "http://queen:8080/api/environments",
            "vendor": "Google Cloud Shell"
        },
        
        # GCP Console APIs
        "/entityServices/OperationsEntityService": {
            "sovereign": "http://temporal:7233/api/operations",
            "vendor": "Google Cloud Console"
        },
        "/entityServices/EmergencymessagingEntityService": {
            "sovereign": "http://khaos-comms:8080/api/alerts",
            "vendor": "Google Cloud Console"
        },
        
        # Default fallback to proxy
        "default": {
            "sovereign": "http://khaos-proxy:8080/translate",
            "vendor": "Unknown Vendor"
        }
    }
    
    def __init__(self, output_dir: str = "generated_tools"):
        self.output_dir = output_dir
        self.template = Template(self.MCP_TOOL_TEMPLATE)
    
    def generate_tool(self, api_pattern: Dict[str, Any]) -> str:
        """Generate MCP tool code from API pattern"""
        
        # Extract pattern data
        method = api_pattern.get('method', 'GET')
        path = api_pattern.get('path', '')
        url = api_pattern.get('url', '')
        params = api_pattern.get('params', {})
        
        # Map to sovereign endpoint
        sovereign_info = self._map_to_sovereign(path)
        
        # Extract parameters
        path_params = self._extract_path_params(path)
        query_params = list(params.keys())
        
        # Build tool data
        tool_data = {
            "tool_class_name": self._pattern_to_classname(path),
            "tool_id": self._pattern_to_id(path),
            "description": self._infer_description(api_pattern),
            "original_endpoint": url,
            "original_vendor": sovereign_info["vendor"],
            "sovereign_endpoint": sovereign_info["sovereign"],
            "method": method,
            "parameters": self._extract_parameters(api_pattern),
            "required_params": json.dumps(self._get_required_params(api_pattern)),
            "path_params": path_params,
            "query_params": query_params,
            "payload_fields": self._extract_payload_fields(api_pattern),
            "source_url": url,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        return self.template.render(**tool_data)
    
    def _map_to_sovereign(self, path: str) -> Dict[str, str]:
        """Map vendor API path to sovereign equivalent"""
        
        # Check for exact match
        if path in self.SOVEREIGN_MAPPINGS:
            return self.SOVEREIGN_MAPPINGS[path]
        
        # Check for partial match
        for pattern, mapping in self.SOVEREIGN_MAPPINGS.items():
            if pattern != "default" and pattern in path:
                return mapping
        
        # Default fallback
        default = self.SOVEREIGN_MAPPINGS["default"]
        return {
            "sovereign": f"{default['sovereign']}?original={path}",
            "vendor": default["vendor"]
        }
    
    def _pattern_to_classname(self, path: str) -> str:
        """Convert API path to Python class name"""
        # Remove leading/trailing slashes
        path = path.strip('/')
        
        # Split by slashes and remove parameters
        parts = [p for p in path.split('/') if not p.startswith('{')]
        
        # Clean each part: remove special characters, keep alphanumeric and underscores
        cleaned_parts = []
        for part in parts:
            # Replace special chars with underscores, then capitalize
            cleaned = re.sub(r'[^a-zA-Z0-9_]', '_', part)
            if cleaned:
                cleaned_parts.append(cleaned)
        
        # Convert to PascalCase
        class_name = ''.join(word.capitalize() for word in cleaned_parts if word)
        
        # Ensure it starts with a letter
        if not class_name or not class_name[0].isalpha():
            class_name = 'Tool' + class_name
        
        return class_name + 'Tool'
    
    def _pattern_to_id(self, path: str) -> str:
        """Convert API path to tool ID"""
        # Remove leading/trailing slashes
        path = path.strip('/')
        
        # Replace slashes with underscores, remove parameters
        parts = [p for p in path.split('/') if not p.startswith('{')]
        tool_id = '_'.join(parts).lower()
        
        # Clean up
        tool_id = re.sub(r'[^a-z0-9_]', '_', tool_id)
        tool_id = re.sub(r'_+', '_', tool_id)
        
        return tool_id
    
    def _infer_description(self, pattern: Dict[str, Any]) -> str:
        """Infer human-readable description"""
        path = pattern.get('path', '')
        method = pattern.get('method', 'GET')
        
        # Extract meaningful parts
        if 'metricDescriptors' in path:
            return "Retrieve metric descriptors and metadata for monitoring"
        elif 'monitoredResourceDescriptors' in path:
            return "Get monitored resource descriptors and types"
        elif 'groups' in path:
            return "Manage resource groups and collections"
        elif 'quota' in path:
            return "Check quota and usage limits"
        elif 'operations' in path.lower():
            return "Query async operation status and results"
        elif 'alert' in path.lower() or 'message' in path.lower():
            return "Manage alerts and emergency notifications"
        else:
            resource = path.split('/')[-1] or 'resource'
            return f"{method} {resource.replace('_', ' ')}"
    
    def _extract_path_params(self, path: str) -> List[str]:
        """Extract path parameters like {project}, {id}, etc."""
        return re.findall(r'\{([^}]+)\}', path)
    
    def _extract_parameters(self, pattern: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract all parameters from pattern"""
        params = []
        
        # Path parameters
        path = pattern.get('path', '')
        for param in self._extract_path_params(path):
            params.append({
                "name": param,
                "type": "string",
                "description": f"Path parameter: {param}",
                "required": True
            })
        
        # Query parameters
        query_params = pattern.get('params', {})
        for name, value in query_params.items():
            param_type = self._infer_type(value)
            params.append({
                "name": name,
                "type": param_type,
                "description": f"Query parameter: {name}",
                "required": False
            })
        
        return params
    
    def _get_required_params(self, pattern: Dict[str, Any]) -> List[str]:
        """Get list of required parameter names"""
        path = pattern.get('path', '')
        return self._extract_path_params(path)
    
    def _extract_payload_fields(self, pattern: Dict[str, Any]) -> List[Dict[str, str]]:
        """Extract payload fields from request body"""
        body = pattern.get('body')
        if not body:
            return []
        
        try:
            data = json.loads(body) if isinstance(body, str) else body
            return [{"name": k} for k in data.keys()]
        except:
            return []
    
    def _infer_type(self, value: Any) -> str:
        """Infer JSON schema type from value"""
        if isinstance(value, bool):
            return "boolean"
        elif isinstance(value, int):
            return "integer"
        elif isinstance(value, float):
            return "number"
        elif isinstance(value, list):
            return "array"
        elif isinstance(value, dict):
            return "object"
        else:
            return "string"
    
    def generate_and_save(self, patterns: List[Dict[str, Any]]) -> List[str]:
        """Generate and save MCP tools from patterns"""
        import os
        
        os.makedirs(self.output_dir, exist_ok=True)
        generated_files = []
        
        for pattern in patterns:
            try:
                # Generate tool code
                code = self.generate_tool(pattern)
                
                # Create filename
                tool_id = self._pattern_to_id(pattern.get('path', ''))
                filename = f"{tool_id}.py"
                filepath = os.path.join(self.output_dir, filename)
                
                # Save to file
                with open(filepath, 'w') as f:
                    f.write(code)
                
                generated_files.append(filepath)
                print(f"Generated: {filepath}")
                
            except Exception as e:
                print(f"Error generating tool for {pattern.get('path', 'unknown')}: {e}")
        
        return generated_files


def main():
    """CLI interface for MCP generation"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate MCP tools from API patterns')
    parser.add_argument('patterns_file', help='JSON file with captured patterns')
    parser.add_argument('-o', '--output-dir', default='generated_tools',
                       help='Output directory for generated tools')
    
    args = parser.parse_args()
    
    # Load patterns
    with open(args.patterns_file, 'r') as f:
        data = json.load(f)
    
    patterns = data.get('patterns', [])
    print(f"Loaded {len(patterns)} patterns")
    
    # Generate tools
    generator = MCPGenerator(output_dir=args.output_dir)
    generated = generator.generate_and_save(patterns)
    
    print(f"\n=== Generation Complete ===")
    print(f"Generated {len(generated)} MCP tools")
    print(f"Output directory: {args.output_dir}")


if __name__ == "__main__":
    main()
