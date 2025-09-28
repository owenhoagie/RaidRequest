#!/usr/bin/env python3
"""
RaidRequest Bot Management Script
Provides easy commands to manage the Discord bot
"""

import os
import sys
import subprocess
import argparse

def get_python_path():
    """Get the path to the virtual environment Python"""
    venv_python = "/Users/owenhoag/Desktop/RaidRequest/RaidRequest/.venv/bin/python"
    if os.path.exists(venv_python):
        return venv_python
    return "python"  # Fallback to system python

def run_setup_check():
    """Run the setup checker"""
    python_path = get_python_path()
    return subprocess.run([python_path, "setup_check.py"])

def run_demo():
    """Run the functionality demo"""
    python_path = get_python_path()
    return subprocess.run([python_path, "demo.py"])

def run_bot():
    """Run the Discord bot"""
    python_path = get_python_path()
    return subprocess.run([python_path, "bot.py"])

def install_deps():
    """Install dependencies"""
    python_path = get_python_path()
    pip_path = python_path.replace("/python", "/pip")
    return subprocess.run([pip_path, "install", "-r", "requirements.txt"])

def create_env_file():
    """Create .env file from template"""
    if os.path.exists(".env"):
        print("⚠️  .env file already exists!")
        response = input("Overwrite? (y/N): ")
        if response.lower() != 'y':
            return
    
    if os.path.exists(".env.example"):
        import shutil
        shutil.copy(".env.example", ".env")
        print("✅ Created .env file from template")
        print("🔧 Please edit .env and add your Discord bot token")
    else:
        with open(".env", "w") as f:
            f.write("BOT_TOKEN=your_discord_bot_token_here\n")
        print("✅ Created .env file")
        print("🔧 Please edit .env and add your Discord bot token")

def main():
    parser = argparse.ArgumentParser(description="RaidRequest Bot Management")
    parser.add_argument("command", choices=[
        "check", "demo", "run", "install", "setup-env"
    ], help="Command to execute")
    
    args = parser.parse_args()
    
    print("🤖 RaidRequest Bot Manager")
    print("=" * 30)
    
    if args.command == "check":
        print("Running setup check...")
        return run_setup_check().returncode
    
    elif args.command == "demo":
        print("Running functionality demo...")
        return run_demo().returncode
    
    elif args.command == "run":
        print("Starting Discord bot...")
        return run_bot().returncode
    
    elif args.command == "install":
        print("Installing dependencies...")
        return install_deps().returncode
    
    elif args.command == "setup-env":
        print("Setting up environment file...")
        create_env_file()
        return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n⏹️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
