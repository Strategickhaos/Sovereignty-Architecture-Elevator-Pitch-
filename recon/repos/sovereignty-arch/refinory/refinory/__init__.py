# ============================================================
# STRATEGICKHAOS DAO LLC • SOVEREIGN SOFTWARE FRAMEWORK
# Copyright © 2025 Domenic G. Garza • All Rights Reserved
# 
# This file is part of the Strategickhaos Autonomous Runtime.
# It may not be copied, modified, distributed, or executed
# except by authorized operators within the Strategickhaos
# governance model and licensing structure.
# 
# Unauthorized use is prohibited. All activity is logged.
# ============================================================

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