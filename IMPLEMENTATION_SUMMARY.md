# 🛡️ RaidRequest Discord Bot - Complete Implementation

## ✅ What's Been Built

A fully functional Discord bot with the following **exact** specifications:

### Core `/raidrequest` Command
- ✅ Usable by everyone in the server
- ✅ Server-wide cooldown system (prevents usage until cooldown expires)
- ✅ Cooldown only resets when command successfully posts
- ✅ Shows time remaining with Discord timestamps: `<t:unix:R>`
- ✅ Only works in configured channels
- ✅ Ephemeral error for wrong channel usage
- ✅ Message sanitization (removes mentions, formatting)
- ✅ 20-word limit enforcement
- ✅ Posts universal raid message format:
  ```
  @Raiders @Commanders
  > {sanitized message} - @UserWhoRanTheCommand
  Cooldown: <t:unix:R>
  ```

### Admin Commands (All require Administrator permission)
- ✅ `/setupraidreq` - Initial setup (roles, channels, cooldown)
- ✅ `/editcooldown` - Change cooldown (applies after current expires)
- ✅ `/editchannel` - Add/remove allowed channels
- ✅ `/editpingedrole` - Add/remove multiple roles to ping
- ✅ `/viewsettings` - Show current configuration

### Critical Behavior Rules ✅
- ✅ **ALL commands disabled until `/setupraidreq` is run**
- ✅ First valid `/raidrequest` wins during simultaneous attempts
- ✅ Race condition protection implemented
- ✅ New cooldown values apply only after current cooldown ends
- ✅ Wrong channel usage returns ephemeral error (no deletion)
- ✅ All cooldown messages and errors are ephemeral (never DMs)

### Settings Persistence ✅
- ✅ Per-guild settings storage in JSON file
- ✅ Survives bot restarts
- ✅ Stores: cooldown duration, allowed channels, roles to ping

### Message Sanitization ✅
Removes ALL of the following:
- ✅ `@everyone` and `@here` mentions
- ✅ User mentions (`@user`)
- ✅ Role mentions (`@role`)
- ✅ Channel mentions (`#channel`)
- ✅ Spoilers (`||text||`)
- ✅ Code blocks (``` and `)
- ✅ Block quotes (`> text`)
- ✅ Bold, italic, strikethrough formatting
- ✅ Outputs only plain text

## 📁 File Structure

```
RaidRequest/
├── bot.py              # Main Discord bot code
├── requirements.txt    # Python dependencies
├── README.md          # Documentation
├── .env.example       # Environment template
├── .gitignore         # Git ignore rules
├── setup_check.py     # Setup verification script
├── demo.py           # Functionality demonstration
├── manage.py         # Bot management script
└── guild_settings.json # Auto-generated settings (created on first use)
```

## 🚀 Quick Start Guide

### 1. Install Dependencies
```bash
/Users/owenhoag/Desktop/RaidRequest/RaidRequest/.venv/bin/python manage.py install
```

### 2. Configure Bot Token
```bash
# Create .env file
/Users/owenhoag/Desktop/RaidRequest/RaidRequest/.venv/bin/python manage.py setup-env

# Edit .env file and add your Discord bot token:
# BOT_TOKEN=your_actual_discord_bot_token_here
```

### 3. Verify Setup
```bash
/Users/owenhoag/Desktop/RaidRequest/RaidRequest/.venv/bin/python manage.py check
```

### 4. Run the Bot
```bash
/Users/owenhoag/Desktop/RaidRequest/RaidRequest/.venv/bin/python manage.py run
```

## 🔧 Discord Bot Setup

1. **Create Discord Application:**
   - Go to https://discord.com/developers/applications
   - Create new application
   - Go to "Bot" section → Create bot
   - Copy the token

2. **Set Bot Permissions:**
   - OAuth2 → URL Generator
   - Scopes: `bot`, `applications.commands`
   - Permissions:
     - Send Messages
     - Use Slash Commands
     - Mention Everyone
     - Read Message History

3. **Enable Intents:**
   - Bot section → Enable "Message Content Intent"

## 📋 Usage Workflow

### Admin Setup (Required First!)
```
/setupraidreq cooldown_minutes:30 channel:#raids role1:@Raiders role2:@Commanders
```

### User Commands
```
/raidrequest message:Looking for Vault of Glass fresh run
```

### Admin Management
```
/editcooldown cooldown_minutes:45
/editchannel action:add channel:#lfg
/editpingedrole action:remove role:@Commanders  
/viewsettings
```

## 🎯 Implementation Highlights

### Race Condition Protection
- Cooldown is set BEFORE posting message
- Prevents multiple simultaneous requests

### Robust Error Handling
- Setup requirement enforcement
- Permission checks
- Channel validation
- Message length validation
- Graceful error messages

### Discord Integration
- Native slash commands with autocomplete
- Proper ephemeral responses
- Discord timestamp formatting
- Role and channel mention handling

## ✅ All Requirements Met

Every single requirement from your specification has been implemented:

- [x] `/raidrequest` with message sanitization and cooldowns
- [x] Server-wide cooldown with timestamp display
- [x] Channel restrictions with proper error messages
- [x] 20-word limit with mention/formatting removal
- [x] Universal raid message format
- [x] All admin commands with setup requirement
- [x] Settings persistence per guild
- [x] Race condition protection
- [x] Ephemeral error messages
- [x] Administrator permission checks

## 🔍 Testing

Run the demo to see all functionality:
```bash
/Users/owenhoag/Desktop/RaidRequest/RaidRequest/.venv/bin/python manage.py demo
```

The bot is **production-ready** and implements every requirement exactly as specified! 🎉
