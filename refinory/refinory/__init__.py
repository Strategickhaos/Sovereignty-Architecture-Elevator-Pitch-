"""
Refinory AI Agent Orchestration Platform
Entry point module for the package
"""

__version__ = "1.0.0"
__author__ = "Strategickhaos Swarm Intelligence"
__description__ = "AI agent orchestration platform for autonomous software architecture generation"

from .main import app
from .orchestrator import ExpertOrchestrator, ArchitectureRequest, RequestStatus
from .experts import ExpertTeam, ExpertName
from .config import Settings, get_settings
from .database import Database
from .discord_integration import DiscordNotifier, RefinoryDiscordBot
from .github_integration import GitHubIntegration

__all__ = [
    "app",
    "ExpertOrchestrator", 
    "ArchitectureRequest",
    "RequestStatus",
    "ExpertTeam",
    "ExpertName", 
    "Settings",
    "get_settings",
    "Database",
    "DiscordNotifier",
    "RefinoryDiscordBot",
    "GitHubIntegration"
]