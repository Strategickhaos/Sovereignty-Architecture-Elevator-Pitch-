"""
Refinory Configuration Management
Centralized settings and environment configuration
"""

import os
from typing import Optional, Dict, Any, List
from pydantic import BaseSettings, Field, validator
import yaml

class RefineryConfig(BaseSettings):
    """Refinory-specific configuration"""
    env: str = Field(default="development", description="Environment (development/staging/production)")
    
    # Service ports
    api_port: int = Field(default=8000, description="FastAPI server port")
    orchestrator_port: int = Field(default=8001, description="Orchestrator service port")
    
    # AI/ML Configuration
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key")
    openai_model: str = Field(default="gpt-4", description="Default OpenAI model")
    anthropic_api_key: Optional[str] = Field(default=None, description="Anthropic API key")
    
    # Expert Configuration
    max_concurrent_experts: int = Field(default=5, description="Maximum concurrent expert tasks")
    expert_timeout: int = Field(default=300, description="Expert task timeout in seconds")
    
    # Workflow Configuration
    enable_temporal: bool = Field(default=True, description="Enable Temporal workflows")
    temporal_namespace: str = Field(default="refinory", description="Temporal namespace")
    
    # Storage Configuration
    artifacts_storage: str = Field(default="local", description="Artifacts storage backend (local/s3)")
    artifacts_path: str = Field(default="./artifacts", description="Local artifacts storage path")
    s3_bucket: Optional[str] = Field(default=None, description="S3 bucket for artifacts")
    
    # Security Configuration
    jwt_secret: Optional[str] = Field(default=None, description="JWT signing secret")
    api_key_header: str = Field(default="X-API-Key", description="API key header name")
    
    class Config:
        env_prefix = "REFINORY_"
        case_sensitive = False

class DatabaseConfig(BaseSettings):
    """Database configuration"""
    host: str = Field(default="localhost", description="PostgreSQL host")
    port: int = Field(default=5432, description="PostgreSQL port")
    database: str = Field(default="refinory", description="Database name")
    username: str = Field(default="refinory", description="Database username")
    password: str = Field(default="refinory123", description="Database password")
    
    # Connection pool settings
    min_connections: int = Field(default=5, description="Minimum connection pool size")
    max_connections: int = Field(default=20, description="Maximum connection pool size")
    
    @property
    def dsn(self) -> str:
        """PostgreSQL connection string"""
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
    
    class Config:
        env_prefix = "DB_"

class RedisConfig(BaseSettings):
    """Redis configuration"""
    host: str = Field(default="localhost", description="Redis host")
    port: int = Field(default=6379, description="Redis port")
    database: int = Field(default=0, description="Redis database number")
    password: Optional[str] = Field(default=None, description="Redis password")
    
    # Connection settings
    max_connections: int = Field(default=20, description="Maximum connection pool size")
    socket_timeout: int = Field(default=5, description="Socket timeout in seconds")
    
    @property
    def url(self) -> str:
        """Redis connection URL"""
        auth = f":{self.password}@" if self.password else ""
        return f"redis://{auth}{self.host}:{self.port}/{self.database}"
    
    class Config:
        env_prefix = "REDIS_"

class QdrantConfig(BaseSettings):
    """Qdrant vector database configuration"""
    host: str = Field(default="localhost", description="Qdrant host")
    port: int = Field(default=6333, description="Qdrant port")
    api_key: Optional[str] = Field(default=None, description="Qdrant API key")
    
    # Collection settings
    default_collection: str = Field(default="refinory_vectors", description="Default collection name")
    vector_size: int = Field(default=1536, description="Vector dimension size")
    
    @property
    def url(self) -> str:
        """Qdrant connection URL"""
        return f"http://{self.host}:{self.port}"
    
    class Config:
        env_prefix = "QDRANT_"

class TemporalConfig(BaseSettings):
    """Temporal workflow configuration"""
    host: str = Field(default="localhost", description="Temporal host")
    port: int = Field(default=7233, description="Temporal port")
    namespace: str = Field(default="refinory", description="Temporal namespace")
    
    # Worker settings
    task_queue: str = Field(default="refinory-architecture", description="Default task queue")
    max_concurrent_activities: int = Field(default=10, description="Maximum concurrent activities")
    
    @property
    def address(self) -> str:
        """Temporal server address"""
        return f"{self.host}:{self.port}"
    
    class Config:
        env_prefix = "TEMPORAL_"

class DiscordConfig(BaseSettings):
    """Discord integration configuration"""
    bot_token: str = Field(description="Discord bot token")
    guild_id: Optional[str] = Field(default=None, description="Discord guild ID")
    
    # Channel configuration
    notifications_channel: Optional[str] = Field(default=None, description="Notifications channel ID")
    dev_feed_channel: Optional[str] = Field(default=None, description="Development feed channel ID")
    
    # Bot settings
    command_prefix: str = Field(default="!", description="Bot command prefix")
    enable_slash_commands: bool = Field(default=True, description="Enable slash commands")
    
    class Config:
        env_prefix = "DISCORD_"

class GitHubConfig(BaseSettings):
    """GitHub integration configuration"""
    token: str = Field(description="GitHub personal access token")
    organization: Optional[str] = Field(default=None, description="GitHub organization")
    
    # PR settings
    auto_create_prs: bool = Field(default=True, description="Automatically create PRs for architectures")
    pr_branch_prefix: str = Field(default="refinory/arch-", description="PR branch prefix")
    
    class Config:
        env_prefix = "GITHUB_"

class MonitoringConfig(BaseSettings):
    """Monitoring and observability configuration"""
    enable_metrics: bool = Field(default=True, description="Enable Prometheus metrics")
    metrics_port: int = Field(default=9090, description="Metrics server port")
    
    # Logging settings
    log_level: str = Field(default="INFO", description="Log level")
    log_format: str = Field(default="json", description="Log format (json/text)")
    
    # Tracing settings
    enable_tracing: bool = Field(default=True, description="Enable distributed tracing")
    jaeger_endpoint: Optional[str] = Field(default=None, description="Jaeger endpoint")
    
    class Config:
        env_prefix = "MONITORING_"

class Settings(BaseSettings):
    """Main application settings"""
    # Environment
    environment: str = Field(default="development", description="Application environment")
    debug: bool = Field(default=True, description="Debug mode")
    
    # Service configuration
    refinory: RefineryConfig = RefineryConfig()
    database: DatabaseConfig = DatabaseConfig()
    redis: RedisConfig = RedisConfig()
    qdrant: QdrantConfig = QdrantConfig()
    temporal: TemporalConfig = TemporalConfig()
    discord: DiscordConfig = DiscordConfig()
    github: GitHubConfig = GitHubConfig()
    monitoring: MonitoringConfig = MonitoringConfig()
    
    # Service URLs (computed properties)
    @property
    def postgres_dsn(self) -> str:
        return self.database.dsn
    
    @property
    def redis_url(self) -> str:
        return self.redis.url
    
    @property
    def qdrant_url(self) -> str:
        return self.qdrant.url
    
    @property
    def temporal_address(self) -> str:
        return self.temporal.address
    
    # Integration tokens
    @property
    def discord_token(self) -> str:
        return self.discord.bot_token
    
    @property
    def github_token(self) -> str:
        return self.github.token
    
    # Load discovery.yml configuration
    @validator("*", pre=True)
    def load_discovery_config(cls, v, field):
        """Load configuration from discovery.yml if available"""
        discovery_path = "/workspaces/Sovereignty-Architecture-Elevator-Pitch-/discovery.yml"
        
        if os.path.exists(discovery_path):
            try:
                with open(discovery_path, "r") as f:
                    discovery = yaml.safe_load(f)
                
                # Extract Refinory configuration if it exists
                refinory_config = discovery.get("refinory", {})
                if refinory_config and field.name == "refinory":
                    # Merge discovery config with environment variables
                    for key, value in refinory_config.items():
                        if hasattr(v, key):
                            setattr(v, key, value)
                
                # Extract Discord configuration
                discord_config = discovery.get("discord", {})
                if discord_config and field.name == "discord":
                    if "bot_token" in discord_config:
                        v.bot_token = discord_config["bot_token"]
                    if "guild_id" in discord_config:
                        v.guild_id = str(discord_config["guild_id"])
                
                # Extract GitHub configuration
                github_config = discovery.get("github", {})
                if github_config and field.name == "github":
                    if "token" in github_config:
                        v.token = github_config["token"]
                    if "organization" in github_config:
                        v.organization = github_config["organization"]
                
            except Exception as e:
                # Silently ignore discovery.yml parsing errors
                pass
        
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

# Global settings instance
_settings: Optional[Settings] = None

def get_settings() -> Settings:
    """Get application settings (singleton)"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings

def reload_settings() -> Settings:
    """Reload settings from environment"""
    global _settings
    _settings = Settings()
    return _settings

# Configuration validation
def validate_configuration(settings: Settings) -> List[str]:
    """Validate configuration and return list of errors"""
    errors = []
    
    # Required tokens
    if not settings.discord_token:
        errors.append("Discord bot token is required")
    
    if not settings.github_token:
        errors.append("GitHub token is required")
    
    # Database connectivity
    if not settings.database.host:
        errors.append("Database host is required")
    
    # AI/ML API keys (at least one required)
    if not settings.refinory.openai_api_key and not settings.refinory.anthropic_api_key:
        errors.append("At least one AI API key (OpenAI or Anthropic) is required")
    
    # Storage configuration
    if settings.refinory.artifacts_storage == "s3" and not settings.refinory.s3_bucket:
        errors.append("S3 bucket is required when using S3 storage")
    
    # Temporal configuration
    if settings.refinory.enable_temporal and not settings.temporal.host:
        errors.append("Temporal host is required when Temporal is enabled")
    
    return errors

# Environment-specific configurations
def get_development_config() -> Dict[str, Any]:
    """Get development environment overrides"""
    return {
        "debug": True,
        "refinory.env": "development",
        "database.database": "refinory_dev",
        "redis.database": 1,
        "monitoring.log_level": "DEBUG"
    }

def get_production_config() -> Dict[str, Any]:
    """Get production environment overrides"""
    return {
        "debug": False,
        "refinory.env": "production",
        "database.min_connections": 10,
        "database.max_connections": 50,
        "redis.max_connections": 50,
        "monitoring.log_level": "INFO",
        "monitoring.enable_tracing": True
    }

def apply_environment_overrides(settings: Settings, environment: str) -> Settings:
    """Apply environment-specific configuration overrides"""
    if environment == "development":
        overrides = get_development_config()
    elif environment == "production":
        overrides = get_production_config()
    else:
        return settings
    
    # Apply overrides (simplified - would need recursive dict merge in practice)
    for key, value in overrides.items():
        if "." in key:
            # Nested configuration
            parts = key.split(".")
            obj = settings
            for part in parts[:-1]:
                obj = getattr(obj, part)
            setattr(obj, parts[-1], value)
        else:
            # Top-level configuration
            setattr(settings, key, value)
    
    return settings