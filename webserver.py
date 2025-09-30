import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"RaidRequest bot is running on port {port}!")
