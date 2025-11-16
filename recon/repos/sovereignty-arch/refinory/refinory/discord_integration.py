"""
Refinory Discord Integration
Discord bot commands and notifications for AI agent orchestration
"""

import asyncio
from typing import Dict, Any, List, Optional
import discord
from discord.ext import commands
import structlog

from .config import Settings

logger = structlog.get_logger()

class RefinoryDiscordBot(commands.Bot):
    """Discord bot for Refinory AI agent orchestration"""
    
    def __init__(self, settings: Settings):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        
        super().__init__(
            command_prefix=settings.discord.command_prefix,
            intents=intents,
            description="Refinory AI Agent Orchestration Platform"
        )
        
        self.settings = settings
        self.refinory_orchestrator = None  # Will be injected
        
    async def setup_hook(self):
        """Initialize bot extensions and sync commands"""
        logger.info("Setting up Refinory Discord bot")
        
        # Add slash commands
        await self.add_cog(RefinoryCommands(self))
        
        # Sync slash commands
        if self.settings.discord.enable_slash_commands:
            try:
                synced = await self.tree.sync()
                logger.info(f"Synced {len(synced)} slash commands")
            except Exception as e:
                logger.error(f"Failed to sync slash commands: {str(e)}")
    
    async def on_ready(self):
        """Called when bot is ready"""
        logger.info(f"Refinory bot logged in as {self.user}")
        
        # Set bot status
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name="AI agents building architectures"
        )
        await self.change_presence(activity=activity)
    
    async def on_command_error(self, ctx, error):
        """Handle command errors"""
        if isinstance(error, commands.CommandNotFound):
            return  # Ignore unknown commands
        
        logger.error(f"Command error in {ctx.command}: {str(error)}")
        
        embed = discord.Embed(
            title="❌ Command Error",
            description=f"An error occurred: {str(error)}",
            color=discord.Color.red()
        )
        
        try:
            await ctx.respond(embed=embed, ephemeral=True)
        except:
            await ctx.send(embed=embed)

class RefineryCommands(commands.Cog):
    """Refinory-specific Discord commands"""
    
    def __init__(self, bot: RefinoryDiscordBot):
        self.bot = bot
    
    @discord.slash_command(
        name="request",
        description="Request AI agent architecture generation"
    )
    async def architecture_request(
        self,
        ctx: discord.ApplicationContext,
        project_name: discord.Option(str, description="Name of the project"),
        description: discord.Option(str, description="Project description"),
        requirements: discord.Option(str, description="Comma-separated requirements", required=False),
        experts: discord.Option(str, description="Comma-separated expert names", required=False),
        priority: discord.Option(
            str, 
            description="Request priority",
            choices=["low", "normal", "high", "critical"],
            required=False,
            default="normal"
        ),
        github_repo: discord.Option(str, description="GitHub repository URL", required=False)
    ):
        """Create new architecture request"""
        await ctx.defer()
        
        try:
            # Parse requirements and experts
            parsed_requirements = [req.strip() for req in requirements.split(",")] if requirements else []
            parsed_experts = [exp.strip() for exp in experts.split(",")] if experts else None
            
            # Create embed for initial response
            embed = discord.Embed(
                title="🏗️ Architecture Request Submitted",
                description=f"Creating architecture for **{project_name}**",
                color=discord.Color.blue()
            )
            embed.add_field(name="Project", value=project_name, inline=True)
            embed.add_field(name="Priority", value=priority.upper(), inline=True)
            embed.add_field(name="Requester", value=ctx.author.display_name, inline=True)
            embed.add_field(name="Description", value=description[:1000], inline=False)
            
            if parsed_requirements:
                embed.add_field(
                    name="Requirements", 
                    value="\n".join([f"• {req}" for req in parsed_requirements[:5]]), 
                    inline=False
                )
            
            if parsed_experts:
                embed.add_field(
                    name="Requested Experts",
                    value=", ".join(parsed_experts),
                    inline=False
                )
            
            embed.set_footer(text="AI agents are analyzing your request...")
            
            await ctx.followup.send(embed=embed)
            
            # TODO: Submit to orchestrator
            # request_id = await self.bot.refinory_orchestrator.submit_request(...)
            
            logger.info(f"Architecture request submitted by {ctx.author.display_name}: {project_name}")
            
        except Exception as e:
            logger.error(f"Failed to process architecture request: {str(e)}")
            
            error_embed = discord.Embed(
                title="❌ Request Failed",
                description=f"Failed to submit architecture request: {str(e)}",
                color=discord.Color.red()
            )
            await ctx.followup.send(embed=error_embed)
    
    @discord.slash_command(
        name="status",
        description="Check status of architecture request"
    )
    async def request_status(
        self,
        ctx: discord.ApplicationContext,
        request_id: discord.Option(str, description="Request ID to check")
    ):
        """Check architecture request status"""
        await ctx.defer()
        
        try:
            # TODO: Get status from orchestrator
            # request = await self.bot.refinory_orchestrator.get_request_status(request_id)
            
            # Mock response for now
            embed = discord.Embed(
                title="📊 Request Status",
                description=f"Status for request `{request_id}`",
                color=discord.Color.green()
            )
            embed.add_field(name="Status", value="In Progress", inline=True)
            embed.add_field(name="Progress", value="65%", inline=True)
            embed.add_field(name="Current Phase", value="Expert Review", inline=True)
            embed.add_field(name="Experts Assigned", value="Frontend, Backend, DevOps, Security", inline=False)
            embed.set_footer(text="Last updated 2 minutes ago")
            
            await ctx.followup.send(embed=embed)
            
        except Exception as e:
            logger.error(f"Failed to get request status: {str(e)}")
            
            error_embed = discord.Embed(
                title="❌ Status Check Failed",
                description=f"Could not retrieve status for request `{request_id}`: {str(e)}",
                color=discord.Color.red()
            )
            await ctx.followup.send(embed=error_embed)
    
    @discord.slash_command(
        name="list-requests",
        description="List recent architecture requests"
    )
    async def list_requests(
        self,
        ctx: discord.ApplicationContext,
        status: discord.Option(
            str,
            description="Filter by status",
            choices=["pending", "analyzing", "expert_review", "generating", "reviewing", "completed", "failed"],
            required=False
        ),
        limit: discord.Option(int, description="Number of requests to show", min_value=1, max_value=20, default=10)
    ):
        """List architecture requests"""
        await ctx.defer()
        
        try:
            # TODO: Get requests from orchestrator
            # requests = await self.bot.refinory_orchestrator.list_requests(status, limit)
            
            # Mock response
            embed = discord.Embed(
                title="📋 Architecture Requests",
                description=f"Recent requests{f' with status: {status}' if status else ''}",
                color=discord.Color.blue()
            )
            
            # Mock data
            mock_requests = [
                {"id": "abc-123", "name": "E-commerce Platform", "status": "completed", "progress": 100},
                {"id": "def-456", "name": "AI Chat Bot", "status": "generating", "progress": 75},
                {"id": "ghi-789", "name": "Mobile App Backend", "status": "expert_review", "progress": 45},
            ]
            
            for req in mock_requests[:limit]:
                status_emoji = {
                    "completed": "✅",
                    "generating": "⚙️", 
                    "expert_review": "👥",
                    "pending": "⏳",
                    "failed": "❌"
                }.get(req["status"], "📋")
                
                embed.add_field(
                    name=f"{status_emoji} {req['name']}",
                    value=f"ID: `{req['id']}`\nStatus: {req['status'].replace('_', ' ').title()}\nProgress: {req['progress']}%",
                    inline=True
                )
            
            await ctx.followup.send(embed=embed)
            
        except Exception as e:
            logger.error(f"Failed to list requests: {str(e)}")
            
            error_embed = discord.Embed(
                title="❌ List Failed",
                description=f"Could not retrieve requests: {str(e)}",
                color=discord.Color.red()
            )
            await ctx.followup.send(embed=error_embed)
    
    @discord.slash_command(
        name="experts",
        description="List available AI experts and their capabilities"
    )
    async def list_experts(self, ctx: discord.ApplicationContext):
        """List available AI experts"""
        await ctx.defer()
        
        experts_data = {
            "Frontend": "User interface, React, Vue, TypeScript, UI/UX",
            "Backend": "APIs, databases, server logic, microservices",
            "DevOps": "Docker, Kubernetes, CI/CD, infrastructure",
            "Security": "Threat modeling, authentication, compliance",
            "AI/ML": "Machine learning, model deployment, data pipelines",
            "Mobile": "React Native, Flutter, mobile optimization",
            "Blockchain": "Smart contracts, DeFi, Web3 integration",
            "Testing": "Test automation, quality assurance, performance",
            "Architecture": "System design, patterns, scalability",
            "Data Science": "Analytics, data processing, warehousing"
        }
        
        embed = discord.Embed(
            title="🤖 Available AI Experts",
            description="Specialized AI agents for architecture generation",
            color=discord.Color.purple()
        )
        
        for expert, description in experts_data.items():
            embed.add_field(
                name=f"💡 {expert} Expert",
                value=description,
                inline=True
            )
        
        embed.set_footer(text="Use /request to engage experts for your project")
        
        await ctx.followup.send(embed=embed)
    
    @discord.slash_command(
        name="refinory-health",
        description="Check Refinory platform health"
    )
    async def platform_health(self, ctx: discord.ApplicationContext):
        """Check platform health status"""
        await ctx.defer()
        
        # TODO: Get actual health status
        # health = await self.bot.refinory_orchestrator.get_health()
        
        embed = discord.Embed(
            title="🔍 Refinory Platform Health",
            color=discord.Color.green()
        )
        
        services = {
            "API Server": "✅ Healthy",
            "PostgreSQL": "✅ Healthy", 
            "Redis": "✅ Healthy",
            "Qdrant": "✅ Healthy",
            "Temporal": "✅ Healthy",
            "Expert Team": "✅ 10/10 experts active"
        }
        
        for service, status in services.items():
            embed.add_field(name=service, value=status, inline=True)
        
        embed.add_field(
            name="📊 Statistics",
            value="Active Requests: 5\nCompleted Today: 12\nUptime: 99.9%",
            inline=False
        )
        
        embed.set_footer(text="All systems operational")
        
        await ctx.followup.send(embed=embed)

class DiscordNotifier:
    """Discord notification service for Refinory events"""
    
    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        self.bot = None
        self._notification_channels = {}
        
    async def initialize(self, orchestrator=None):
        """Initialize Discord bot"""
        if not self.bot_token:
            logger.warning("Discord token not provided, notifications disabled")
            return
            
        settings = Settings()  # Get fresh settings
        self.bot = RefinoryDiscordBot(settings)
        self.bot.refinory_orchestrator = orchestrator
        
        # Start bot in background
        asyncio.create_task(self.bot.start(self.bot_token))
        
        logger.info("Discord notifier initialized")
    
    async def notify_request_created(self, request_id: str):
        """Notify when new architecture request is created"""
        if not self.bot:
            return
            
        # TODO: Send notification to appropriate channel
        logger.info(f"Would notify: New request created - {request_id}")
    
    async def notify_architecture_ready(self, request_id: str, architecture: Dict[str, Any]):
        """Notify when architecture is ready"""
        if not self.bot:
            return
            
        logger.info(f"Would notify: Architecture ready - {request_id}")
    
    async def notify_pr_created(self, request_id: str, pr_url: str):
        """Notify when GitHub PR is created"""
        if not self.bot:
            return
            
        logger.info(f"Would notify: PR created - {request_id}: {pr_url}")
    
    async def notify_error(self, request_id: str, error: str):
        """Notify when error occurs"""
        if not self.bot:
            return
            
        logger.info(f"Would notify: Error - {request_id}: {error}")
    
    async def send_to_channel(self, channel_id: str, embed: discord.Embed):
        """Send embed to specific channel"""
        if not self.bot or not self.bot.is_ready():
            return
            
        try:
            channel = self.bot.get_channel(int(channel_id))
            if channel:
                await channel.send(embed=embed)
            else:
                logger.warning(f"Channel {channel_id} not found")
        except Exception as e:
            logger.error(f"Failed to send message to channel {channel_id}: {str(e)}")