import discord
from discord.ext import commands
from discord import app_commands
import json
import asyncio
import time
import re
import os
from datetime import datetime, timezone
from typing import Dict, List, Optional

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
# Allow the bot to mention everyone and all roles
allowed_mentions = discord.AllowedMentions(everyone=True, roles=True, users=True)
bot = commands.Bot(command_prefix='!', intents=intents, allowed_mentions=allowed_mentions)

# Global storage for settings and cooldowns
guild_settings: Dict[int, Dict] = {}
cooldown_data: Dict[int, Dict] = {}  # guild_id: {"end_time": timestamp}

SETTINGS_FILE = "guild_settings.json"

def load_settings():
    """Load guild settings from JSON file"""
    global guild_settings
    try:
        with open(SETTINGS_FILE, 'r') as f:
            guild_settings = json.load(f)
            # Convert string keys back to int
            guild_settings = {int(k): v for k, v in guild_settings.items()}
    except FileNotFoundError:
        guild_settings = {}

def save_settings():
    """Save guild settings to JSON file"""
    with open(SETTINGS_FILE, 'w') as f:
        # Convert int keys to string for JSON compatibility
        settings_to_save = {str(k): v for k, v in guild_settings.items()}
        json.dump(settings_to_save, f, indent=2)

def is_setup_complete(guild_id: int) -> bool:
    """Check if setup has been completed for a guild"""
    return guild_id in guild_settings and guild_settings[guild_id].get('setup_complete', False)

def sanitize_message(message: str) -> str:
    """Sanitize the message by removing mentions and formatting"""
    # Remove @everyone and @here mentions
    message = re.sub(r'@(everyone|here)', '', message, flags=re.IGNORECASE)
    
    # Remove user mentions (<@!123456789> or <@123456789>)
    message = re.sub(r'<@!?\d+>', '', message)
    
    # Remove role mentions (<@&123456789>)
    message = re.sub(r'<@&\d+>', '', message)
    
    # Remove channel mentions (<#123456789>)
    message = re.sub(r'<#\d+>', '', message)
    
    # Remove formatting
    # Remove spoilers ||text||
    message = re.sub(r'\|\|([^|]+)\|\|', r'\1', message)
    
    # Remove code blocks ```text```
    message = re.sub(r'```[^`]*```', '', message)
    
    # Remove inline code `text`
    message = re.sub(r'`([^`]+)`', r'\1', message)
    
    # Remove block quotes > text
    message = re.sub(r'^>\s*', '', message, flags=re.MULTILINE)
    
    # Remove bold **text** and __text__
    message = re.sub(r'\*\*([^*]+)\*\*', r'\1', message)
    message = re.sub(r'__([^_]+)__', r'\1', message)
    
    # Remove italic *text* and _text_
    message = re.sub(r'\*([^*]+)\*', r'\1', message)
    message = re.sub(r'_([^_]+)_', r'\1', message)
    
    # Remove strikethrough ~~text~~
    message = re.sub(r'~~([^~]+)~~', r'\1', message)
    
    # Remove underline and other formatting
    message = re.sub(r'~~([^~]+)~~', r'\1', message)
    
    # Clean up extra whitespace
    message = ' '.join(message.split())
    
    return message.strip()

def is_on_cooldown(guild_id: int) -> tuple[bool, Optional[int]]:
    """Check if guild is on cooldown and return cooldown end time"""
    if guild_id not in cooldown_data:
        return False, None
    
    current_time = int(time.time())
    end_time = cooldown_data[guild_id].get('end_time', 0)
    
    if current_time >= end_time:
        # Cooldown expired, remove it
        del cooldown_data[guild_id]
        return False, None
    
    return True, end_time

def set_cooldown(guild_id: int, duration: int):
    """Set cooldown for a guild"""
    end_time = int(time.time()) + duration
    cooldown_data[guild_id] = {'end_time': end_time}

@bot.event
async def on_ready():
    """Bot ready event"""
    load_settings()
    print(f'{bot.user} has logged in and is ready!')
    
    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(f'Failed to sync commands: {e}')

@bot.tree.command(name="setupraidreq", description="Initial setup for raid request system")
@app_commands.describe(
    cooldown_minutes="Cooldown duration in minutes",
    channel="Channel where raid requests are allowed",
    role1="First role to ping (required)",
    role2="Second role to ping (optional)",
    role3="Third role to ping (optional)"
)
async def setup_raid_req(
    interaction: discord.Interaction,
    cooldown_minutes: int,
    channel: discord.TextChannel,
    role1: discord.Role,
    role2: Optional[discord.Role] = None,
    role3: Optional[discord.Role] = None
):
    """Setup the raid request system"""
    # Check if user has admin permissions
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ You need administrator permissions to use this command.", ephemeral=True)
        return
    
    # Validate inputs
    if cooldown_minutes < 1:
        await interaction.response.send_message("❌ Cooldown must be at least 1 minute.", ephemeral=True)
        return
    
    # Prepare roles list
    roles = [role1.id]
    if role2:
        roles.append(role2.id)
    if role3:
        roles.append(role3.id)
    
    # Save settings
    guild_id = interaction.guild.id
    guild_settings[guild_id] = {
        'setup_complete': True,
        'cooldown_seconds': cooldown_minutes * 60,
        'allowed_channels': [channel.id],
        'pinged_roles': roles
    }
    save_settings()
    
    # Format role mentions for display with special handling for @everyone
    role_mentions_list = []
    
    # Handle role1 (required)
    if role1.name == "@everyone":
        role_mentions_list.append("@everyone")
    else:
        role_mentions_list.append(f"<@&{role1.id}>")
    
    # Handle role2 (optional)
    if role2:
        if role2.name == "@everyone":
            role_mentions_list.append("@everyone")
        else:
            role_mentions_list.append(f"<@&{role2.id}>")
    
    # Handle role3 (optional)
    if role3:
        if role3.name == "@everyone":
            role_mentions_list.append("@everyone")
        else:
            role_mentions_list.append(f"<@&{role3.id}>")
    
    role_mentions = ", ".join(role_mentions_list)
    
    await interaction.response.send_message(
        f"✅ **Raid Request System Setup Complete!**\n\n"
        f"**Settings:**\n"
        f"• Cooldown: {cooldown_minutes} minutes\n"
        f"• Allowed Channel: {channel.mention}\n"
        f"• Roles to ping: {role_mentions}\n\n"
        f"The system is now active! Users can use `/raidrequest` in {channel.mention}.",
        ephemeral=True
    )

@bot.tree.command(name="raidrequest", description="Request a raid with a custom message")
@app_commands.describe(message="Your raid request message (max 20 words)")
async def raid_request(interaction: discord.Interaction, message: str):
    """Main raid request command"""
    guild_id = interaction.guild.id
    
    # Check if setup is complete
    if not is_setup_complete(guild_id):
        await interaction.response.send_message("❌ The raid request system has not been set up yet. An administrator needs to run `/setupraidreq` first.", ephemeral=True)
        return
    
    settings = guild_settings[guild_id]
    
    # Check if command is used in allowed channel
    if interaction.channel.id not in settings['allowed_channels']:
        channel_mentions = [f"<#{ch_id}>" for ch_id in settings['allowed_channels']]
        await interaction.response.send_message(
            f"❌ This command can only be used in: {', '.join(channel_mentions)}",
            ephemeral=True
        )
        return
    
    # Check cooldown
    on_cooldown, end_time = is_on_cooldown(guild_id)
    if on_cooldown:
        await interaction.response.send_message(
            f"⏰ This command is on cooldown. Try again <t:{end_time}:R>.",
            ephemeral=True
        )
        return
    
    # Sanitize and validate message
    sanitized_msg = sanitize_message(message)
    
    # Check word count
    word_count = len(sanitized_msg.split())
    if word_count > 20:
        await interaction.response.send_message(
            f"❌ Your message is too long ({word_count} words). Please keep it to 20 words or less.",
            ephemeral=True
        )
        return
    
    if not sanitized_msg.strip():
        await interaction.response.send_message("❌ Your message cannot be empty after removing formatting and mentions.", ephemeral=True)
        return
    
    # Set cooldown BEFORE posting (to prevent race conditions)
    set_cooldown(guild_id, settings['cooldown_seconds'])
    
    # Build role mentions with special handling for @everyone
    role_mentions_list = []
    for role_id in settings['pinged_roles']:
        role = interaction.guild.get_role(role_id)
        if role and role.name == "@everyone":
            # Check if bot has permission to mention everyone
            if interaction.guild.me.guild_permissions.mention_everyone:
                role_mentions_list.append("@everyone")
            else:
                role_mentions_list.append("@everyone (no permission)")
        else:
            role_mentions_list.append(f"<@&{role_id}>")
    
    role_mentions = ' '.join(role_mentions_list)
    
    # Calculate cooldown end time for display
    cooldown_end = int(time.time()) + settings['cooldown_seconds']
    
    # Create the raid message
    raid_message = (
        f"{role_mentions}\n"
        f"> {sanitized_msg} - {interaction.user.mention}\n\n"
        f"**Cooldown:** <t:{cooldown_end}:R>"
    )
    
    # Send the public raid message
    await interaction.response.send_message(raid_message)

@bot.tree.command(name="editcooldown", description="Change the cooldown duration")
@app_commands.describe(cooldown_minutes="New cooldown duration in minutes")
async def edit_cooldown(interaction: discord.Interaction, cooldown_minutes: int):
    """Edit the cooldown duration"""
    guild_id = interaction.guild.id
    
    # Check if user has admin permissions
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ You need administrator permissions to use this command.", ephemeral=True)
        return
    
    # Check if setup is complete
    if not is_setup_complete(guild_id):
        await interaction.response.send_message("❌ Please run `/setupraidreq` first to set up the system.", ephemeral=True)
        return
    
    # Validate input
    if cooldown_minutes < 1:
        await interaction.response.send_message("❌ Cooldown must be at least 1 minute.", ephemeral=True)
        return
    
    # Update settings
    guild_settings[guild_id]['cooldown_seconds'] = cooldown_minutes * 60
    save_settings()
    
    await interaction.response.send_message(
        f"✅ Cooldown updated to {cooldown_minutes} minutes. "
        f"This will take effect after the current cooldown expires.",
        ephemeral=True
    )

@bot.tree.command(name="editchannel", description="Update allowed channels")
@app_commands.describe(
    action="Add or remove a channel",
    channel="The channel to add or remove"
)
@app_commands.choices(action=[
    app_commands.Choice(name="Add", value="add"),
    app_commands.Choice(name="Remove", value="remove")
])
async def edit_channel(interaction: discord.Interaction, action: str, channel: discord.TextChannel):
    """Edit allowed channels"""
    guild_id = interaction.guild.id
    
    # Check if user has admin permissions
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ You need administrator permissions to use this command.", ephemeral=True)
        return
    
    # Check if setup is complete
    if not is_setup_complete(guild_id):
        await interaction.response.send_message("❌ Please run `/setupraidreq` first to set up the system.", ephemeral=True)
        return
    
    settings = guild_settings[guild_id]
    
    if action == "add":
        if channel.id not in settings['allowed_channels']:
            settings['allowed_channels'].append(channel.id)
            save_settings()
            await interaction.response.send_message(f"✅ Added {channel.mention} to allowed channels.", ephemeral=True)
        else:
            await interaction.response.send_message(f"❌ {channel.mention} is already in the allowed channels list.", ephemeral=True)
    
    elif action == "remove":
        if len(settings['allowed_channels']) <= 1:
            await interaction.response.send_message("❌ Cannot remove the last allowed channel. At least one channel must be configured.", ephemeral=True)
            return
        
        if channel.id in settings['allowed_channels']:
            settings['allowed_channels'].remove(channel.id)
            save_settings()
            await interaction.response.send_message(f"✅ Removed {channel.mention} from allowed channels.", ephemeral=True)
        else:
            await interaction.response.send_message(f"❌ {channel.mention} is not in the allowed channels list.", ephemeral=True)

@bot.tree.command(name="editpingedrole", description="Add or remove roles to ping")
@app_commands.describe(
    action="Add or remove a role",
    role="The role to add or remove"
)
@app_commands.choices(action=[
    app_commands.Choice(name="Add", value="add"),
    app_commands.Choice(name="Remove", value="remove")
])
async def edit_pinged_role(interaction: discord.Interaction, action: str, role: discord.Role):
    """Edit pinged roles"""
    guild_id = interaction.guild.id
    
    # Check if user has admin permissions
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ You need administrator permissions to use this command.", ephemeral=True)
        return
    
    # Check if setup is complete
    if not is_setup_complete(guild_id):
        await interaction.response.send_message("❌ Please run `/setupraidreq` first to set up the system.", ephemeral=True)
        return
    
    settings = guild_settings[guild_id]
    
    # Get proper role display name
    role_display = "@everyone" if role.name == "@everyone" else role.mention
    
    if action == "add":
        if role.id not in settings['pinged_roles']:
            settings['pinged_roles'].append(role.id)
            save_settings()
            await interaction.response.send_message(f"✅ Added {role_display} to pinged roles.", ephemeral=True)
        else:
            await interaction.response.send_message(f"❌ {role_display} is already in the pinged roles list.", ephemeral=True)
    
    elif action == "remove":
        if len(settings['pinged_roles']) <= 1:
            await interaction.response.send_message("❌ Cannot remove the last pinged role. At least one role must be configured.", ephemeral=True)
            return
        
        if role.id in settings['pinged_roles']:
            settings['pinged_roles'].remove(role.id)
            save_settings()
            await interaction.response.send_message(f"✅ Removed {role_display} from pinged roles.", ephemeral=True)
        else:
            await interaction.response.send_message(f"❌ {role_display} is not in the pinged roles list.", ephemeral=True)

@bot.tree.command(name="viewsettings", description="View current raid request settings")
async def view_settings(interaction: discord.Interaction):
    """View current settings"""
    guild_id = interaction.guild.id
    
    # Check if user has admin permissions
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ You need administrator permissions to use this command.", ephemeral=True)
        return
    
    # Check if setup is complete
    if not is_setup_complete(guild_id):
        await interaction.response.send_message("❌ The raid request system has not been set up yet. Run `/setupraidreq` first.", ephemeral=True)
        return
    
    settings = guild_settings[guild_id]
    
    # Format settings for display
    cooldown_minutes = settings['cooldown_seconds'] // 60
    
    channel_mentions = []
    for ch_id in settings['allowed_channels']:
        channel = interaction.guild.get_channel(ch_id)
        if channel:
            channel_mentions.append(channel.mention)
        else:
            channel_mentions.append(f"<#{ch_id}> (deleted)")
    
    role_mentions = []
    for role_id in settings['pinged_roles']:
        role = interaction.guild.get_role(role_id)
        if role:
            if role.name == "@everyone":
                role_mentions.append("@everyone")
            else:
                role_mentions.append(role.mention)
        else:
            role_mentions.append(f"<@&{role_id}> (deleted)")
    
    # Check current cooldown status
    on_cooldown, end_time = is_on_cooldown(guild_id)
    cooldown_status = f"<t:{end_time}:R>" if on_cooldown else "Not active"
    
    embed = discord.Embed(
        title="🛡️ Raid Request Settings",
        color=discord.Color.blue(),
        timestamp=datetime.now(timezone.utc)
    )
    
    embed.add_field(
        name="⏰ Cooldown Duration",
        value=f"{cooldown_minutes} minutes",
        inline=True
    )
    
    embed.add_field(
        name="📺 Allowed Channels",
        value="\n".join(channel_mentions) if channel_mentions else "None configured",
        inline=True
    )
    
    embed.add_field(
        name="🔔 Pinged Roles",
        value="\n".join(role_mentions) if role_mentions else "None configured",
        inline=True
    )
    
    embed.add_field(
        name="⏳ Current Cooldown",
        value=cooldown_status,
        inline=False
    )
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

if __name__ == "__main__":
    # Get bot token from environment variable or use placeholder
    token = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN')
    
    if token == 'YOUR_BOT_TOKEN':
        print("⚠️  Please set your BOT_TOKEN environment variable or replace 'YOUR_BOT_TOKEN' in the code!")
        print("   You can create a .env file with: BOT_TOKEN=your_actual_bot_token")
        exit(1)
    
    bot.run(token)
