import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")
DATABASE_URL = os.getenv("DATABASE_URL")
ENV = os.getenv("ENV", "development")
CHANNEL_ANNOUNCE = 1463563610482806855
CHANNEL_VOICE_PANEL = 1472182125728895027
CHANNEL_TEST = 1471916423751274538


if ENV == "development":
    print("Rodando em DEV")
else:
    print("Rodando em PRODUÇÂO")
if GUILD_ID:
    GUILD_ID = int(GUILD_ID)
