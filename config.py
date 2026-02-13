import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")
DATABASE_URL = os.getenv("DATABASE_URL")

if GUILD_ID:
    GUILD_ID = int(GUILD_ID)