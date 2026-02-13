import discord
from discord.ext import commands
from config import TOKEN, GUILD_ID
from views.shop_view import ShopView
from database.db import Database
import os

TOKEN = os.getenv("DISCORD_TOKEN")


class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix="!", intents=intents)


    async def setup_hook(self):
        self.db = Database()
        await self.db.connect()
        await self.db._create_tables()
        # await self.tree.sync()  # sincroniza comandos globalmente
        await self.load_extension("cogs.quiz")
        await self.load_extension("cogs.util")
        await self.load_extension("cogs.moderacao")
        await self.load_extension("cogs.shop")
        await self.load_extension("cogs.grow")
        await self.load_extension("cogs.meuplano")
        await self.load_extension("cogs.mapa")
        await self.load_extension("cogs.auto_reply")
        

        self.add_view(ShopView(self.db))

        if GUILD_ID:
            guild = discord.Object(id=GUILD_ID)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
        else:
            await self.tree.sync()


bot = Bot()

@bot.event
async def on_ready():
    print(f"Conectado como {bot.user}")


bot.run(TOKEN)
