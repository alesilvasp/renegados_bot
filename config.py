import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")
DATABASE_URL = os.getenv("DATABASE_URL")
ENV = os.getenv("ENV", "development")

if ENV == "development":
    print("Rodando em DEV")
else:
    print("Rodando em PRODUÇÂO")
if GUILD_ID:
    GUILD_ID = int(GUILD_ID)