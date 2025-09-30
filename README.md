# RaidRequest Bot

This is a Discord bot designed to manage raid requests and integrate with Firebase for persistent storage.

## Features

- Discord bot functionality.
- Firebase integration for data storage.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Add your environment variables to the `.env` file:
   ```properties
   BOT_TOKEN=YOUR_DISCORD_BOT_TOKEN
   FIREBASE_URL=YOUR_FIREBASE_URL
   FIREBASE_SECRET=YOUR_FIREBASE_SECRET
   ```

3. Run the bot:
   ```bash
   python bot.py
   ```

## Files

- `bot.py`: Main bot logic.
- `.env`: Environment variables.
- `requirements.txt`: Python dependencies.
