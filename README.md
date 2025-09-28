# RaidRequest Discord Bot

A Discord bot that manages raid requests with cooldowns, channel restrictions, and role pinging.

## Features

- **Raid Request Command**: `/raidrequest` with message sanitization and cooldowns
- **Admin Setup**: Complete configuration system for guilds
- **Channel Restrictions**: Only works in configured channels
- **Role Pinging**: Customizable roles to ping on raid requests
- **Cooldown System**: Server-wide cooldowns with timestamp display
- **Persistent Settings**: Guild settings saved to JSON file

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a Discord application and bot:
   - Go to https://discord.com/developers/applications
   - Create a new application
   - Go to the "Bot" section
   - Create a bot and copy the token
   - Enable necessary intents (Message Content Intent)

3. Configure the bot:
   - Replace `YOUR_BOT_TOKEN` in `bot.py` with your actual bot token
   - Or create a `.env` file with `BOT_TOKEN=your_token_here`

4. Invite the bot to your server:
   - Go to OAuth2 > URL Generator
   - Select "bot" and "applications.commands" scopes
   - Select necessary permissions:
     - Send Messages
     - Use Slash Commands
     - **Mention Everyone** ⚠️ **CRITICAL for role pings to work**
     - Read Message History

## Commands

### Admin Commands (Administrator permission required)

- `/setupraidreq` - Initial setup (required before other commands work)
  - `cooldown_minutes`: How long between raid requests
  - `channel`: Which channel to allow raid requests in
  - `role1`: First role to ping (required)
  - `role2`: Second role to ping (optional)
  - `role3`: Third role to ping (optional)

- `/editcooldown` - Change cooldown duration
- `/editchannel` - Add/remove allowed channels
- `/editpingedrole` - Add/remove roles to ping
- `/viewsettings` - View current configuration

### User Commands

- `/raidrequest` - Request a raid
  - `message`: Your raid message (max 20 words, sanitized automatically)

## Message Sanitization

The bot automatically removes:
- @everyone and @here mentions
- User mentions (@user)
- Role mentions (@role)
- Channel mentions (#channel)
- Formatting (bold, italic, code blocks, spoilers, etc.)
- Block quotes

## Cooldown System

- Server-wide cooldown starts when a raid request is successfully posted
- Shows remaining time using Discord timestamps
- New cooldown settings apply after current cooldown expires
- First valid request wins during simultaneous attempts

## File Structure

- `bot.py` - Main bot code
- `requirements.txt` - Python dependencies
- `guild_settings.json` - Auto-generated settings storage
- `README.md` - This file

## Quick Start

1. **Install dependencies:**
```bash
python manage.py install
```

2. **Set up environment:**
```bash
python manage.py setup-env
# Then edit .env file with your bot token
```

3. **Check setup:**
```bash
python manage.py check
```

4. **Run the bot:**
```bash
python manage.py run
```

## Management Commands

- `python manage.py install` - Install dependencies
- `python manage.py setup-env` - Create .env file from template
- `python manage.py check` - Verify setup is complete
- `python manage.py demo` - Show functionality demonstration
- `python manage.py run` - Start the Discord bot

## Running the Bot

```bash
python bot.py
# OR
python manage.py run
```

The bot will automatically sync slash commands when it starts up.
