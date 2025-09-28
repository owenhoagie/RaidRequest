#!/usr/bin/env python3
"""
Setup script for RaidRequest Discord Bot
"""

import os
import sys

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"   Current version: {sys.version}")
        return False
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import discord
        print("✅ discord.py is installed")
        return True
    except ImportError:
        print("❌ discord.py is not installed")
        print("   Run: pip install -r requirements.txt")
        return False

def check_token():
    """Check if bot token is configured"""
    # Check for .env file
    if os.path.exists('.env'):
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            pass
    
    token = os.getenv('BOT_TOKEN')
    if not token or token == 'your_discord_bot_token_here':
        print("❌ Bot token is not configured")
        print("   1. Create a .env file (copy from .env.example)")
        print("   2. Add your bot token: BOT_TOKEN=your_actual_token")
        print("   3. Or set the BOT_TOKEN environment variable")
        return False
    
    print("✅ Bot token is configured")
    return True

def main():
    """Main setup check"""
    print("🤖 RaidRequest Discord Bot Setup Check")
    print("=" * 40)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies), 
        ("Bot Token", check_token)
    ]
    
    all_passed = True
    for name, check_func in checks:
        print(f"\nChecking {name}...")
        if not check_func():
            all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("✅ All checks passed! You can now run the bot with: python bot.py")
    else:
        print("❌ Some checks failed. Please fix the issues above before running the bot.")
    
    return all_passed

if __name__ == "__main__":
    main()
